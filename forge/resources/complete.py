from tastypie.resources import Resource
from django.db import connection
from forge.resources.card import similarity_check


class CompleteResource(Resource):
    class Meta:
        resource_name = 'complete'
        allowed_methods = ['get']
        detail_allowed_methods = []
        limit = 10

    def get_list(self, request, **kwargs):
        meta = self._meta
        query = """
            SELECT f.name
            FROM forge_cardftsindex AS i
            JOIN oracle_cardface AS f ON f.id = i.card_face_id
            WHERE TRUE
                {search_filter}
            ORDER BY f.name
            LIMIT %(limit)s
        """
        filters = dict(search_filter='')
        params = dict(limit=meta.limit)

        cursor = connection.cursor()
        if request.GET.get('q', ''):
            search = request.GET.get('q', '')
            search, original = similarity_check(cursor, search)
            search = search.strip(' \n\t').split(' ')
            search = [u'{0}:A*'.format(s) for s in search]
            params['term'] = u' & '.join(search)
            filters['search_filter'] = 'AND i.fts @@ to_tsquery(%(term)s)'

        cursor.execute(query.format(**filters), params)
        objects = [r[0] for r in cursor.fetchall()]

        to_be_serialized = objects
        return self.create_response(request, to_be_serialized)
