import re
import urllib

from django.db import connection
from django.core.paginator import Paginator, InvalidPage
from django.conf.urls.defaults import *
from tastypie.resources import ModelResource
from oracle.models import CardL10n, Color

def int2bin(n, count=24):
    """returns the binary of integer n, using count number of digits"""
    return "".join([str((n >> y) & 1) for y in range(count-1, -1, -1)])

class CardResource(ModelResource):
    class Meta:
        resource_name = 'card'
        queryset = CardL10n.objects.all()
        allowed_methods = ['get']

    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search/$" %
                self._meta.resource_name,
                self.wrap_view('get_search'),
                name="api_get_search"),
        ]

    def get_search(self, request, **kwargs):
        """
        Performs fts search on Card using CardFtsIndex table
        """

        cursor = connection.cursor()
        meta = {}
        
        # prepare base query
        query = """
            select {select_type} from forge_cardftsindex i
            join oracle_cardl10n l on (i.card_face_id = l.card_face_id and l.language='en')
            where 
                True
                {search_filter}
                {set_filter}
                {color_filter}
                {type_filter}
        """

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
            meta['query'] = search
            meta['original_query'] = original
            search = search.split(' ')
            search = ["%s:*" % s for s in search]
            search = " & ".join(search)
            filters['search_filter'] = 'AND i.fts @@ to_tsquery(%s)'
            args.append(search)

        if request.GET.get('sets', ''):
            sets = [str(int(s)) for s in request.GET['sets'].split(',')]
            sets = '|'.join(sets)
            sets = "AND i.sets @@ '%s'::query_int" % sets
            filters['set_filter'] = sets

        if request.GET.get('color', ''):
            color = request.GET.get('color').lower()
            identity = Color(color).identity
            identity_query = [ str(1<<i) for i in range(6) if (i<<i) & identity ]
            operator = '&' if 'a' in color else '|'
            identity_query = "'%s'::query_int" % operator.join(identity_query)
            # identity_query = '1 | 12 | 56'
            filters['color_filter'] = 'AND color_identity_idx @@ %s' % identity_query

        if request.GET.get('type', ''):
            type_query = request.GET.get('type').strip(' \t\n,').split(',')
            type_query = ['%s:B*' % q for q in type_query]
            type_query = ' | '.join(type_query)
            # type_query = 'red:B* & creature:B* with:B* flying:B*'
            filters['type_filter'] = 'AND i.fts @@ to_tsquery(%s)'
            args.append(type_query)


        # fetch total objects count and build metadata
        cursor.execute(query.format(select_type="count(*)", **filters), args)
        total_count = cursor.fetchone()[0]
        limit = int(request.GET.get('limit', 20))
        offset = int(request.GET.get('offset', 0))
        if total_count < limit + offset:
            next_url = None
        else:
            next_url = "/api/v1/card/search/?" + urllib.urlencode(dict(
                format='json',
                limit = limit,
                offset = limit + offset,
                q = request.GET.get('q', ''),
                types = request.GET.get('types', ''),
                color = request.GET.get('color', ''),
                sets = request.GET.get('sets', ''),
            )).replace('+', ' ')

        meta.update(
            next = next_url,
            total_count = total_count,
            limit = limit,
            offset=offset
        )
        
        # make an ordered and limited query
        query = query + """
            order by  ts_rank_cd( 
                ARRAY[1.0,0.9,0.8,0.7], 
                i.fts,
                to_tsquery(%s)
            )
            limit %s 
            offset %s
        """
        args += [search, limit, offset]
        query = query.format(select_type = 'l.*', **filters)
        print query, args
        query = CardL10n.objects.raw(query, args)

        
        
        # serialize objects for tastypy response
        objects = []
        for result in query:
            bundle = self.build_bundle(obj=result, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        return self.create_response(request, dict(
            objects = objects,
            meta = meta
        ))

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
