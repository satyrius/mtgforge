from scrapy.contracts import Contract
from scrapy.http import Request
from scrapy.item import BaseItem
from scrapy.exceptions import ContractFail
import json
from urlparse import urlparse, parse_qsl, urlunparse
from urllib import urlencode


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


class PartialContract(ItemContract):
    '''Contracts to check one of the result items data has expected json.
        @partial {\
            "foo": "value",\
        }
    '''
    name = 'partial'

    def post_process(self, output):
        data = []
        for x in output:
            if isinstance(x, BaseItem):
                try:
                    self.testcase_post.maxDiff = None
                    expected = set(self.expected_json.items())
                    item = set(dict(x).items())
                    self.testcase_post.assertTrue(expected <= item)
                    return
                except AssertionError:
                    data.append(x)
        raise ContractFail('Expected data\n{}\nnot found in output\n{}'.format(
            self.expected_json, data))


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


class MetaContract(Contract):
    '''Pass request meta
    @meta name Anton Egorov
    '''
    name = 'meta'

    def adjust_request_args(self, kwargs):
        if 'meta' not in kwargs or not kwargs['meta']:
            kwargs['meta'] = {}
        kwargs['meta'][self.args[0]] = u' '.join(self.args[1:])
        return kwargs


class QueryContract(Contract):
    '''Add given query param to the request url
    @url_query name Anton Egorov
    '''
    name = 'url_query'

    def adjust_request_args(self, kwargs):
        if 'url' in kwargs:
            url = list(urlparse(kwargs['url']))
            query = dict(parse_qsl(url[4]))
            query[self.args[0]] = u' '.join(self.args[1:])
            url[4] = urlencode(query)
            kwargs['url'] = urlunparse(url)
        return kwargs


class ItemsClassContract(Contract):
    '''Contract to check that output countains accurate number of items of
    given Class. Example:

    @items MyItem 2
    '''
    name = 'items'

    def post_process(self, output):
        cls, cnt = self.args
        count = 0
        for x in output:
            if isinstance(x, BaseItem) and type(x).__name__ == cls:
                count += 1

        if count != int(cnt):
            raise ContractFail('Expected to get {} of {}, got {}'.format(
                cnt, cls, count))


class RequestContract(Contract):
    '''Contract to check returned request url and meta. To assert meta
    pass key-value pairs right after url. Keys should starts with @.

    @request http://example.com @foo 1 @bar Lorem ipsum
    '''
    name = 'request'

    def __init__(self, *args, **kwargs):
        super(RequestContract, self).__init__(*args, **kwargs)
        self.url = self.args[0]
        self.meta = {}
        k = None
        for x in self.args[1:]:
            if x.startswith('@'):
                k = x[1:]
            elif k:
                self.meta.setdefault(k, []).append(x)
        self.meta = {k: u' '.join(v) for k, v in self.meta.items()}

    def post_process(self, output):
        for x in output:
            if isinstance(x, Request):
                if x.url == self.url:
                    for k, v in self.meta.items():
                        got = x.meta.get(k)
                        if got != v:
                            raise ContractFail(
                                'Request with url {} has the following value '
                                'for meta argument "{}": "{}". '
                                'Expected "{}"'.format(x.url, k, got, v))
                    return
        raise ContractFail('Request with url {} expected'.format(self.url))
