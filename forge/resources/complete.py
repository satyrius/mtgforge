from tastypie.cache import SimpleCache
from tastypie.resources import Resource

from forge.models import FtsSuggest
from forge.resources.base import cached_response


class CompleteResource(Resource):
    class Meta:
        resource_name = 'complete'
        allowed_methods = ['get']
        detail_allowed_methods = []
        cache = SimpleCache()
        limit = 10

    @cached_response
    def get_list(self, request, **kwargs):
        meta = self._meta
        term = request.GET.get('q', '').strip()
        words = FtsSuggest.objects.filter(term__startswith=term)\
                          .order_by('-weight', 'term')\
                          .values_list('term', flat=True)[:meta.limit]

        to_be_serialized = words
        return self.create_response(request, to_be_serialized)
