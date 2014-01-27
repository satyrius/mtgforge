import re

from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request

from crawler.items import CardImageItem
from crawler.pipelines.cards import get_or_create_card_image


class ArtPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if 'art' in item:
            url = re.sub('&?options=rotate90', '', item['art'])
            yield Request(url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if image_paths:
            if len(image_paths) > 1:
                raise DropItem('Item cannot contain more than one art image')
            item['art_path'] = self.store._get_filesystem_path(image_paths[0])
        return item


class CardImagePipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, CardImageItem):
            get_or_create_card_image(item)
        return item
