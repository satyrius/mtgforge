import json
import os
import re
import urllib2
import uuid

from django.conf import settings
from django.core.files.storage import Storage
from django.db import models
from ostrovok_common.utils.http import fetch_get, post_multipart
from ostrovok_common.utils.thumbs import cdn_thumbnail
from south.modelsinspector import add_introspection_rules


class CDNReadableImageStorage(Storage):
    def _open(self, name, mode='rb'):
        return fetch_get(cdn_thumbnail(name, format='orig', secure=False))

    def save(self, name, content):
        return name

    def exists(self, name):
        return False

    def url(self, name):
        return cdn_thumbnail(name, format='orig', secure=False)


class CDNFileField(models.FileField):
    def __init__(self, verbose_name=None, name=None,
            upload_to=settings.MEDIA_ROOT, storage_path=None, **kwargs):
        self.storage_path = storage_path
        storage = CDNReadableImageStorage()
        super(CDNFileField, self).__init__(verbose_name, name, upload_to,
                storage, **kwargs)

    def pre_save(self, model_instance, add):
        file = super(CDNFileField, self).pre_save(model_instance, add)
        if not file:
            return file

        # Cut CDN prefix
        cdn_prefix = '^(' + settings.CDN_URL_HTTP_ONLY.rstrip('/')\
                   + '|' + settings.CDN_URL_SECURABLE.rstrip('/')\
                   + ')/t/orig/'
        if re.match(cdn_prefix, file.name):
            file = '/' + re.sub(cdn_prefix, '', file.name).lstrip('/')

        return file

add_introspection_rules([
    (
        [CDNFileField],   # Class(es) these apply to
        [],               # Positional arguments (not used)
        {                 # Keyword argument
            'storage_path': ['storage_path', {'default': None}],
        },
    ),
], ['^contrib\.cdn\.CDNFileField'])


class HeadRequest(urllib2.Request):
    def get_method(self):
        return 'HEAD'

def get_image_type(url):
    response = urllib2.urlopen(HeadRequest(url))
    content_type = response.headers['Content-Type'].split(';')[0].lower()
    if not content_type.startswith('image/'):
        raise Exception('{0} is no an image'.format(url))
    return content_type.split('/', 2)[-1]


def save_to_cdn(url, path, formats):
    content = fetch_get(url)

    extension = get_image_type(url)
    cdn_file_name = ('{}.{}'.format(uuid.uuid4().get_hex(), extension)).encode('ascii')
    fields = [('url', os.path.join(path, cdn_file_name))]
    for t in [('formats', f) for f in formats]:
        fields.append(t)

    status, status_text, json_response = post_multipart(
        settings.IMAGE_STORAGE_HOST,
        '/upload/',
        fields,
        [('file', cdn_file_name, content)],
    )

    json_response = json.loads(json_response)
    return json_response['url']
