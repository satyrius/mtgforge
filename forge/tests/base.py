import urllib
import urls  # to be able to reverse resource url


def get_uri(resource, **kwargs):
    uri = resource.get_resource_list_uri()
    if kwargs:
        uri += '?' + urllib.urlencode(kwargs)
    return uri
