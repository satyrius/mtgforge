import re

from django.core.files.base import File
from scrapy.contrib.pipeline.files import FilesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request

from oracle.forms import CardImageForm
from oracle.models import CardImage
from crawler.spiders.gatherer import get_mvid


class CardImagePipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        if 'art' in item:
            url = re.sub('&?options=rotate90', '', item['art'])
            yield Request(url)

    def item_completed(self, results, item, info):
        images = [(x['path'], x['url']) for ok, x in results if ok]
        if images:
            if len(images) > 1:
                raise DropItem('Item cannot contain more than one art image')

            path, url = images[0]
            mvid = item['mvid'] if 'mvid' in item else get_mvid(url)
            if mvid is None:
                raise DropItem(
                    u'Image url {url} does not contain multiverse id'.format(
                        url=url))

            try:
                img = CardImage.objects.get(mvid=mvid)
            except CardImage.DoesNotExist:
                cif = CardImageForm(data={'mvid': mvid, 'scan': url})
                img = cif.save()

            if not img.file:
                self._save_file(img, path)

        return item

    def _save_file(self, img, path):
        abs_path = self.store._get_filesystem_path(path)
        name = '{0}.image'.format(img.mvid)
        with open(abs_path, 'rb') as f:
            img.file.save(name, File(f))
