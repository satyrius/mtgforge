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
        """
        filters = dict(search_filter='')
        args = []

        cursor = connection.cursor()
        if request.GET.get('q', ''):
            search = request.GET.get('q', '')
            search, original = similarity_check(cursor, search)
            search = search.strip(' \n\t').split(' ')
            search = [u'{0}:A*'.format(s) for s in search]
            search = u' & '.join(search)
            filters['search_filter'] = 'AND i.fts @@ to_tsquery(%s)'
            args.append(search)

        # Set limits
        query += """
            LIMIT %s
        """
        args.append(meta.limit)

        cursor.execute(query.format(**filters), args)
        objects = [r[0] for r in cursor.fetchall()]

        to_be_serialized = objects
        return self.create_response(request, to_be_serialized)
