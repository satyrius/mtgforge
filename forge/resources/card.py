import re
import urllib

from django.conf.urls.defaults import url
from django.core.urlresolvers import NoReverseMatch
from django.db import connection
from forge.resources.base import ModelResource
from oracle.models import CardFace, Color, CardSet, CardImage
from tastypie.exceptions import BadRequest


def get_art_url(name):
    return CardImage().file.storage.url(name)


class CardResource(ModelResource):
    class Meta:
        resource_name = 'cards'
        queryset = CardFace.objects.all()
        list_allowed_methods = []
        details_allowed_methods = ['get']

    def dehydrate(self, bundle):
        bundle.data['scan'] = bundle.obj.scan
        if bundle.obj.file:
            bundle.data['scan'] = get_art_url(bundle.obj.file)
        bundle.data['rank'] = bundle.obj.rank
        return bundle

    def dehydrate_colors(self, bundle):
        return bundle.obj.color_names

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
            SELECT DISTINCT ON ({rank}, r.card_id)
                f.*,
                img.*,
                {rank} AS rank
            FROM forge_cardftsindex AS i
            JOIN oracle_cardface AS f ON f.id = i.card_face_id
            JOIN oracle_cardrelease AS r ON r.card_id = f.card_id
            JOIN oracle_cardset AS cs ON cs.id = r.card_set_id
            JOIN oracle_cardimage AS img ON img.mvid = r.mvid
            WHERE
                TRUE
                {search_filter}
                {set_filter}
                {rarity_filter}
                {color_filter}
                {type_filter}
                {cmc_filter}
            ORDER BY {rank} DESC, r.card_id, cs.released_at DESC
        """
        count_query = "SELECT COUNT(1) FROM ({query}) AS t".format(query=query)

        params = {}
        filters = dict(
            search_filter='',
            set_filter='',
            rarity_filter='',
            color_filter='',
            type_filter='',
            cmc_filter='',
            rank='1',
        )

        # FULL TEXT SEARCH filter
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
            filters['search_filter'] = 'AND i.fts @@ to_tsquery(%(q)s)'
            filters['rank'] = 'ts_rank_cd(array[0.1,0.5,1,0.8], i.fts, to_tsquery(%(q)s), 4)'
            params['q'] = search

        # SET filter
        acronyms = get_commaseparated_param(request, 'set')
        if acronyms:
            extra_url_args['set'] = acronyms
            set_ids = CardSet.objects.filter(
                acronym__in=acronyms).values_list('id', flat=True)
            if len(set_ids) != len(acronyms):
                raise BadRequest('Make shure all set acronyms exist')
            filters['set_filter'] = "AND i.sets @@ '{0}'::query_int".format(
                '|'.join(map(str, set_ids)))

        # RARITY filter
        rarity = get_commaseparated_param(request, 'rarity')
        if rarity:
            extra_url_args['rarity'] = rarity
            filters['rarity_filter'] = 'AND i.fts @@ to_tsquery(%(rarity)s)'
            params['rarity'] = u' | '.join(
                [u'%s:B*' % q.strip(' \n\t') for q in rarity])

        # COLOR filter
        color = get_commaseparated_param(request, 'color')
        if color:
            extra_url_args['color'] = color
            if 'a' in color:
                color.remove('a')
                operator = u' & '
            else:
                operator = u' | '

            identity_query = [str(Color.MAP[c]) for c in color]
            identity_query = u"'%s'::query_int" % operator.join(identity_query)
            filters['color_filter'] = u'AND i.color_identity_idx @@ {0}'.format(
                identity_query)

        # TYPE filter
        type_query = get_commaseparated_param(request, 'type')
        if type_query:
            extra_url_args['type'] = type_query
            type_query = [u'%s:B*' % q.strip(' \n\t') for q in type_query]
            filters['type_filter'] = 'AND i.fts @@ to_tsquery(%(type)s)'
            params['type'] = u' | '.join(type_query)

        # CMC filter
        cmc = get_commaseparated_param(request, 'cmc')
        if cmc:
            extra_url_args['cmc'] = cmc
            cmc = map(int, cmc)
            cmc_filter = 'AND (i.cmc = ANY(%(cmc)s){higher_cost})'
            higher_cost = 7 in cmc and ' OR i.cmc > 7' or ''
            filters['cmc_filter'] = cmc_filter.format(higher_cost=higher_cost)
            params['cmc'] = cmc

        # fetch total objects count and build metadata
        cursor.execute(count_query.format(**filters), params)
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
            limit %(limit)s
            offset %(offset)s
        """
        params.update(dict(limit=limit, offset=offset))
        query = query.format(**filters)
        query = CardFace.objects.raw(query, params)

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


def get_commaseparated_param(request, name):
    # Parameter may be passed as '&type=creature&type=artifact'
    params_list = request.GET.getlist(name, [])
    # Join list with comma for compatibility with commaseparates values
    values = ','.join(params_list).split(',')
    return filter(lambda v: v is not None and v != '', values)
