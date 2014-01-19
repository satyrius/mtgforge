from crawler.items import CardSetItem


class BaseCardSetItemPipeline(object):
    def _process_item(self, item, spider):
        raise NotImplementedError

    def process_item(self, item, spider):
        if isinstance(item, CardSetItem):
            self._process_item(item, spider)
        return item


class CardSetsPipeline(BaseCardSetItemPipeline):
    def _process_item(self, item, spider):
        pass
