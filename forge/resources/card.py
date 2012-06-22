import urllib

from django.core.paginator import Paginator, InvalidPage
from django.conf.urls.defaults import *
from tastypie.resources import ModelResource
from oracle.models import CardL10n


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

        query_args = dict(
            tables = [
                'oracle_cardftsindex',
                'oracle_cardface',
                'oracle_card'
            ],
            where = [ """
                oracle_cardface.id = oracle_cardl10n.card_face_id AND
                oracle_card.id = oracle_cardface.card_id AND
                oracle_cardftsindex.card_id = oracle_card.id AND
                oracle_cardftsindex.fts @@ to_tsquery('%s')
                
            """ % search]
        )
        query = CardL10n.objects.extra(**query_args)

        total_count = query.count()
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
            ))

        
        # make ordering here (fucken djanga orm)
        query_args['where'][0] += """
                ORDER BY
                ts_rank_cd( 
                    ARRAY[1.0,0.9,0.8,0.7], 
                    oracle_cardftsindex.fts,
                    to_tsquery('%s')
                )
        """ % search

        objects = []
        for result in query[offset:limit+offset]:
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

