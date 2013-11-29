from scrapy.contrib.exporter import BaseItemExporter


class ItemNameExporter(BaseItemExporter):
    def __init__(self, file, **kwargs):
        self._configure(kwargs, dont_fail=True)
        self.file = file

    def export_item(self, item):
        self.file.write(item['name'] + '\n')
