import re
import urllib

from django.conf.urls.defaults import url
from django.core.urlresolvers import NoReverseMatch
from django.db import connection

from forge.resources import ModelResource
from oracle.models import CardFace, Color


class CardResource(ModelResource):
    class Meta:
        resource_name = 'cards'
        queryset = CardFace.objects.all()
        list_allowed_methods = []
        details_allowed_methods = ['get']

    def dehydrate(self, bundle):
        bundle.data['scan'] = bundle.obj.scan
        return bundle

    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search/$" %
                self._meta.resource_name,
                self.wrap_view('get_search'),
                name="api_get_search"),
        ]

    def get_resource_search_uri(self):
        """
        Returns a URL specific to this resource's search endpoint.
        """
        kwargs = {
            'resource_name': self._meta.resource_name,
        }

        if self._meta.api_name is not None:
            kwargs['api_name'] = self._meta.api_name

        try:
            return self._build_reverse_url("api_get_search", kwargs=kwargs)
        except NoReverseMatch:
            return None

    def get_search(self, request, **kwargs):
        """
        Performs fts search on Card using CardFtsIndex table
        """

        cursor = connection.cursor()
        meta = {}
        extra_url_args = {}  # for building next and prev links

        # prepare base query
        query = """
            SELECT DISTINCT ON ({rank}, r.card_id) f.*,
                COALESCE(l.name, f.name) AS name,
                COALESCE(l.type_line, f.type_line) AS type_line,
                COALESCE(l.rules, f.rules) AS rules,
                COALESCE(l.flavor, f.flavor) AS flavor,
                COALESCE(l.scan, r.scan) AS scan
            FROM forge_cardftsindex AS i
            JOIN oracle_cardface AS f ON f.id = i.card_face_id
            JOIN oracle_cardrelease AS r ON r.card_id = f.card_id
            JOIN oracle_cardset cs ON cs.id = r.card_set_id
            LEFT JOIN oracle_cardl10n AS l
                ON f.id = l.card_face_id
                AND l.language = 'en'
            WHERE
                TRUE
                {search_filter}
                {set_filter}
                {color_filter}
                {type_filter}
                {cmc_filter}
            ORDER BY {rank} DESC, r.card_id, cs.released_at DESC
        """
        count_query = "SELECT COUNT(1) FROM ({query}) AS t".format(query=query)

        args = []
        filters = dict(
            search_filter='',
            set_filter='',
            color_filter='',
            type_filter='',
            cmc_filter='',
            rank='1',
        )

        # custom filters
        if request.GET.get('q', ''):
            search = request.GET.get('q', '')
            search, original = similarity_check(cursor, search)
            search = search.strip(' \n\t')
            extra_url_args['q'] = search
            meta['query'] = search
            meta['original_query'] = original
            search = search.split(' ')
            search = [u'%s:*' % s for s in search]
            search = u' & '.join(search)
            filters['search_filter'] = 'AND i.fts @@ to_tsquery(%s)'
            filters['rank'] = 'ts_rank_cd(array[0.1,0.7,0.8,0.9], i.fts, to_tsquery(%s), 4)'
            args.append(search)
            args.append(search)

        sets = [str(int(s)) for s in request.GET.getlist('set', [])]
        if sets:
            extra_url_args['set'] = sets
            sets = '|'.join(sets)
            sets = "AND i.sets @@ '%s'::query_int" % sets
            filters['set_filter'] = sets

        colors = request.GET.getlist('c', [])
        if colors:
            extra_url_args['c'] = colors
            if 'a' in colors:
                colors.remove('a')
                operator = u' & '
            else:
                operator = u' | '

            identity_query = [str(Color.MAP[c]) for c in colors]
            identity_query = u"'%s'::query_int" % operator.join(identity_query)
            filters['color_filter'] = u'AND color_identity_idx @@ {0}'.format(
                identity_query)

        type_query = request.GET.getlist('type', [])
        if type_query:
            extra_url_args['type'] = type_query
            type_query = [u'%s:B*' % q.strip(' \n\t') for q in type_query]
            type_query = u' | '.join(type_query)
            filters['type_filter'] = 'AND i.fts @@ to_tsquery(%s)'
            args.append(type_query)

        if 'cmc' in request.GET:
            try:
                cmc = int(request.GET.get('cmc'))
            except ValueError:
                pass
            else:
                extra_url_args['cmc'] = str(cmc)
                filters['cmc_filter'] = 'AND i.cmc = %s'
                args.append(cmc)

        # fetch total objects count and build metadata
        if filters['search_filter']:
            args.append(search)
        cursor.execute(count_query.format(**filters), args)
        total_count = cursor.fetchone()[0]
        limit = int(request.GET.get('limit', 20))
        offset = int(request.GET.get('offset', 0))
        if total_count < limit + offset:
            next_url = None
        else:
            next_url = self.get_resource_search_uri() + '?' + urllib.urlencode(
                dict(
                    format='json',
                    limit=limit,
                    offset=limit + offset,
                    **extra_url_args
                ), doseq=True)

        meta.update(
            next=next_url,
            total_count=total_count,
            limit=limit,
            offset=offset
        )

        # make an ordered and limited query
        query = query + """
            limit %s
            offset %s
        """
        args += [limit, offset]
        query = query.format(**filters)
        query = CardFace.objects.raw(query, args)

        # serialize objects for tastypy response
        objects = []
        for result in query:
            bundle = self.build_bundle(obj=result, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        to_be_serialized = dict(
            objects=objects,
            meta=meta
        )
        to_be_serialized = self.alter_list_data_to_serialize(
            request, to_be_serialized)
        return self.create_response(request, to_be_serialized)


def similarity_check(cursor, query):
    original = query
    query = re.split('[^\w]', query.lower(), flags=re.I)
    cursor.execute("""
        SELECT DISTINCT ON (sim.keyword) src.kw, sim.keyword
        FROM (
            SELECT UNNEST(ARRAY[%s]) kw
        ) src, forge_cardsimilarity sim
        WHERE
            NOT EXISTS(
                SELECT id
                FROM forge_cardsimilarity
                WHERE keyword = src.kw
            )
            AND sim.keyword %% src.kw
        ORDER BY sim.keyword, similarity(sim.keyword, src.kw)
    """, [query])
    modifications = cursor.fetchall()
    modified = original
    for source, changed in modifications:
        modified = modified.replace(source, changed)

    return modified, original
