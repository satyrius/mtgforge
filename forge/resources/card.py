import urllib
from django.conf.urls.defaults import url
from django.core.urlresolvers import NoReverseMatch
from tastypie.exceptions import BadRequest
from tastypie.utils import trailing_slash

from forge.fts import FtsQuery
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
        if hasattr(bundle.obj, 'scan'):
            bundle.data['thumb'] = bundle.obj.scan
        if hasattr(bundle.obj, 'file') and bundle.obj.file:
            bundle.data['thumb'] = bundle.data['original'] = \
                get_art_url(bundle.obj.file)
        if hasattr(bundle.obj, 'thumb') and bundle.obj.thumb:
            bundle.data['thumb'] = get_thumb_url(bundle.obj.thumb)
        if hasattr(bundle.obj, 'rank'):
            bundle.data['rank'] = bundle.obj.rank
        return bundle

    def dehydrate_colors(self, bundle):
        return bundle.obj.color_names

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
        Performs fts search on Card using CardFtsIndex table
        """

        extra_url_args = {}  # for building next and prev links

        query = FtsQuery()
        if request.GET.get('q', ''):
            search = request.GET['q'].strip(' \n\t')
            query.add_term(q=search)
            extra_url_args['q'] = search

        acronyms = get_commaseparated_param(request, 'set')
        if acronyms:
            query.add_term(sets=acronyms)
            if query.meta['sets_filtered'] != len(acronyms):
                raise BadRequest('Make shure all set acronyms exist')
            extra_url_args['set'] = acronyms

        rarity = get_commaseparated_param(request, 'rarity')
        if rarity:
            query.add_term(rarity=rarity)
            extra_url_args['rarity'] = rarity

        color = get_commaseparated_param(request, 'color')
        if color:
            query.add_term(colors=color)
            extra_url_args['color'] = color

        type_query = get_commaseparated_param(request, 'type')
        if type_query:
            query.add_term(types=type_query)
            extra_url_args['type'] = type_query

        cmc = get_commaseparated_param(request, 'cmc')
        if cmc:
            query.add_term(cmc=cmc)
            extra_url_args['cmc'] = cmc

        meta = query.meta.copy()

        # fetch total objects count and build metadata
        total_count = query.execute_count()
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

        # serialize objects for tastypie response
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
