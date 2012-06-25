from tastypie.resources import ModelResource as TastypieModelResource


class ModelResource(TastypieModelResource):

    def alter_list_data_to_serialize(self, request, data):
        data[self._meta.resource_name] = data.pop('objects')
        return data
