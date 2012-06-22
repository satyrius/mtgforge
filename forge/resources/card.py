import urllib

from django.db import connection
from django.core.paginator import Paginator, InvalidPage
from django.conf.urls.defaults import *
from tastypie.resources import ModelResource
from oracle.models import CardFtsIndex, CardL10n, CardFace


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

        # search = 'cheap red creature'
        search = request.GET.get('q', '')
        search = search.strip(' \n\t')
        search = search.split(' ')
        search = ["%s:*" % s for s in search]
        search = " & ".join(search)
        # search = 'cheap:* & red:* & creature:*'
        
        # prepare base query
        query = """
            select {select_type} from oracle_card c
            join oracle_cardftsindex i on (c.id = i.card_id)
            join oracle_cardface f on (f.card_id = c.id and f.place = 'front')
            join oracle_cardl10n l on (f.id = l.card_face_id)
            {set_joins}
            where 
                i.fts @@ to_tsquery(%s) AND
                l.language = 'en'
                {set_filter}
        """

        args = [search]
        filters = dict(
            set_filter = '',
            set_joins = '',
            color_filter = ''
        )

        if 'set' in request.GET:
            filters['set_joins'] = "join oracle_cardrelease r on (l.card_release_id = r.id)"    
            filters['set_filter'] = "AND r.card_set_id = any(%s)"
            args.append([int(s) for s in request.GET['set'].split(',')])



        # fetch total objects count and build metadata
        cursor = connection.cursor()
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
                q = request.GET.get('q')
            )).replace('+', ' ')


        
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
        query = CardL10n.objects.raw(query, args)

        
        
        # serialize objects for tastypy response
        objects = []
        for result in query:
            bundle = self.build_bundle(obj=result, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        return self.create_response(request, dict(
            object_list = objects,
            meta = dict(
                next = next_url,
                total_count = total_count,
                limit = limit,
                offset=offset
            )
        ))

