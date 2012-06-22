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
        search = search.split(' ')
        search = ["%s:*" % s for s in search]
        search = " & ".join(search)
        # search = 'cheap:* & red:* & creature:*'
        query = CardL10n.objects.extra(
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

        paginator = self._meta.paginator_class(
            request.GET,
            query,
            self.get_resource_list_uri(),
            limit=self._meta.limit
        )
        page = paginator.page()
        objects = []
        for result in page['objects']:
            bundle = self.build_bundle(obj=result, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        page['objects'] = objects
        return self.create_response(request, page)
