import re
import urllib

from django.db import connection
from django.conf.urls.defaults import url
from django.core.urlresolvers import NoReverseMatch
from oracle.models import CardL10n, Color
from . import ModelResource


class CardResource(ModelResource):
    class Meta:
        resource_name = 'cards'
        queryset = CardL10n.objects.all()
        list_allowed_methods = []
        details_allowed_methods = ['get']

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
        extra_url_args = {} # for building next and prev links

        # prepare base query
        query = """
            select distinct on (r.card_id) l.* from forge_cardftsindex i
            join oracle_cardl10n l on (i.card_face_id = l.card_face_id and l.language='en')
            join oracle_cardrelease r on r.id = l.card_release_id
            join oracle_cardset cs on cs.id = r.card_set_id
            where
                True
                {search_filter}
                {set_filter}
                {color_filter}
                {type_filter}
            order by r.card_id, cs.released_at desc
        """
        count_query = """select count(1) from ({query}) as t""".format(query=query)

        args = []
        filters = dict(
            search_filter = '',
            set_filter = '',
            set_joins = '',
            color_filter = '',
            type_filter = ''
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
            search = ["%s:*" % s for s in search]
            search = " & ".join(search)
            filters['search_filter'] = 'AND i.fts @@ to_tsquery(%s)'
            args.append(search)

        sets = [str(int(s)) for s in request.GET.getlist('sets', [])]
        if sets:
            extra_url_args['sets'] = sets
            sets = '|'.join(sets)
            sets = "AND i.sets @@ '%s'::query_int" % sets
            filters['set_filter'] = sets

        colors = request.GET.getlist('color', [])
        if colors:
            extra_url_args['color'] = colors
            if 'a' in colors:
                colors.remove('a')
                operator = ' & '
            else:
                operator = ' | '

            identity_query = [str(Color.MAP[c]) for c in colors]
            identity_query = "'%s'::query_int" % operator.join(identity_query)
            # identity_query = '1 | 12 | 56'
            filters['color_filter'] = 'AND color_identity_idx @@ %s' % identity_query

        type_query = request.GET.getlist('type', [])
        if type_query:
            extra_url_args['type'] = type_query
            type_query = ['%s:B*' % q.strip(' \n\t') for q in type_query]
            type_query = ' | '.join(type_query)
            # type_query = 'red:B* & creature:B* with:B* flying:B*'
            filters['type_filter'] = 'AND i.fts @@ to_tsquery(%s)'
            print filters['type_filter'], type_query
            args.append(type_query)


        # fetch total objects count and build metadata
        cursor.execute(count_query.format(**filters), args)
        total_count = cursor.fetchone()[0]
        limit = int(request.GET.get('limit', 20))
        offset = int(request.GET.get('offset', 0))
        if total_count < limit + offset:
            next_url = None
        else:
            next_url = self.get_resource_search_uri() + '?' + urllib.urlencode(dict(
                format='json',
                limit = limit,
                offset = limit + offset,
                **extra_url_args
            ), doseq=True)


        meta.update(
            next = next_url,
            total_count = total_count,
            limit = limit,
            offset=offset
        )

        # make an ordered and limited query
        query = query + """, ts_rank_cd(
                ARRAY[1.0,0.9,0.8,0.7],
                i.fts,
                to_tsquery(%s)
            )
            limit %s
            offset %s
        """
        args += [search, limit, offset]
        query = query.format(**filters)
        query = CardL10n.objects.raw(query, args)

        # serialize objects for tastypy response
        objects = []
        for result in query:
            bundle = self.build_bundle(obj=result, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        to_be_serialized = dict(
            objects = objects,
            meta = meta
        )
        to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)
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
