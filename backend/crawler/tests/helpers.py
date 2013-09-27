import codecs
from os import path


def get_html_fixture(name):
    fname = path.join(path.dirname(__file__), 'html_fixtures', name + '.html')
    return codecs.open(fname).read().strip()
