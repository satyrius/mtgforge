from scrapy.contracts import Contract
from scrapy.item import BaseItem
from scrapy.exceptions import ContractFail
import json


class ItemContract(Contract):
    """ Contract to check scraped items data to be equal to expected json
        @item_json {\
            "foo": "value",\
            "bar": 1,\
            "desc": "multi\\nline\\nstring"\
        }
    """

    name = 'item_json'

    def __init__(self, *args, **kwargs):
        super(ItemContract, self).__init__(*args, **kwargs)
        # Glue splited contract args back to parse it as json instead
        arg = u' '.join(args[1:])
        self.expected_json = json.loads(arg)

    def post_process(self, output):
        for x in output:
            if isinstance(x, BaseItem):
                try:
                    self.testcase_post.maxDiff = None
                    self.testcase_post.assertEqual(dict(x), self.expected_json)
                except AssertionError as e:
                    raise ContractFail(e)
