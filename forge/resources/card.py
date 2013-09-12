import urllib
from django.conf import settings
from django.conf.urls.defaults import url
from django.core.urlresolvers import NoReverseMatch
from tastypie.utils import trailing_slash

from forge import fts
from forge.resources.base import ModelResource
from oracle.models import CardFace, CardImage, CardImageThumb


def get_art_url(name):
    return CardImage().file.storage.url(name)


def get_thumb_url(name):
    return CardImageThumb().file.storage.url(name)


class CardResource(ModelResource):
    class Meta:
        resource_name = 'cards'
        queryset = CardFace.objects.all()
        list_allowed_methods = []
        details_allowed_methods = ['get']

    def dehydrate(self, bundle):
        bundle.data['rules'] = bundle.data['rules'].split('\n')

        # Card image
        if hasattr(bundle.obj, 'scan'):
            bundle.data['thumb'] = bundle.obj.scan
        if hasattr(bundle.obj, 'file') and bundle.obj.file:
            bundle.data['thumb'] = bundle.data['original'] = \
                get_art_url(bundle.obj.file)
        if hasattr(bundle.obj, 'thumb') and bundle.obj.thumb:
            bundle.data['thumb'] = get_thumb_url(bundle.obj.thumb)

        # Debug ranking
        if settings.DEBUG_SERP:
            debug = {}
            for k in ['rank', 'ranks', 'card_number', 'card_set_id']:
                if hasattr(bundle.obj, k):
                    debug[k] = getattr(bundle.obj, k)
            bundle.data['debug'] = debug

        return bundle

    def dehydrate_colors(self, bundle):
        return bundle.obj.color_short_names

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" %
                (self._meta.resource_name, trailing_slash()),
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
        Performs fts search on CardFace using CardFtsIndex table
        """
        filters = {}
        search = request.GET.get('q', '').strip(' \n\t')
        if search:
            filters['q'] = search
        for k in ['set', 'rarity', 'color', 'type', 'cmc']:
            values = get_commaseparated_param(request, k)
            if values:
                filters[k] = values

        query = fts.FtsQuery().add_term(**filters)
        meta = query.meta.copy()

        # Fetch total objects count and build metadata
        total_count = query.execute_count()
        limit = int(request.GET.get('limit', 20))
        offset = int(request.GET.get('offset', 0))
        if total_count < limit + offset:
            next_url = None
        else:
            filters.update(format='json', limit=limit, offset=limit + offset)
            next_url = u'{}?{}'.format(
                self.get_resource_search_uri(),
                urllib.urlencode(filters, doseq=True))

        # Update response meta
        meta.update(
            next=next_url,
            total_count=total_count,
            limit=limit,
            offset=offset
        )

        # Serialize objects for tastypie response
        objects = []
        for result in query.execute(limit, offset):
            bundle = self.build_bundle(obj=result, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        to_be_serialized = self.alter_list_data_to_serialize(
            request, {'objects': objects, 'meta': meta})
        return self.create_response(request, to_be_serialized)


def get_commaseparated_param(request, name):
    # Parameter may be passed as '&type=creature&type=artifact'
    params_list = request.GET.getlist(name, [])
    # Join list with comma for compatibility with commaseparates values
    values = ','.join(params_list).split(',')
    return filter(lambda v: v is not None and v != '', values)
