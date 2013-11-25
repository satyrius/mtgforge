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


class FieldContract(Contract):
    '''Contract to check that item contain named field with given value. First
    word is a field name, and the rest threated as string field value.
    @field name Anton Egorov
    @field language Python
    '''
    name = 'field'

    def __init__(self, *args, **kwargs):
        super(FieldContract, self).__init__(*args, **kwargs)
        self.field_name = args[1]
        self.field_value = u' '.join(args[2:]).replace('\\n', '\n')

    def post_process(self, output):
        for x in output:
            if isinstance(x, BaseItem):
                f = self.field_name
                v = self.field_value
                if not f in x:
                    if v == '':
                        # Empty value expected
                        continue
                    else:
                        raise ContractFail("'{}' field is missing".format(f))
                try:
                    self.testcase_post.assertEqual(x[f], v)
                except AssertionError, e:
                    raise ContractFail(e)
