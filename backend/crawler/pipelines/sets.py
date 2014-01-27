import datetime
import re
from xact import xact
from scrapy.exceptions import DropItem

from crawler.items import CardSetItem
from crawler.models import CardSetAlias
from oracle.forms import CardSetForm
from oracle.models import CardSet


class InvalidData(DropItem):
    pass


class BaseCardSetItemPipeline(object):
    def _process_item(self, item, spider):
        raise NotImplementedError

    def process_item(self, item, spider):
        if isinstance(item, CardSetItem):
            self._process_item(item, spider)
        return item


def generate_slug(name):
    name = name.lower()

    # Normalize core set counting
    word2num = [
        (('one', 'first', 'i'), 1),
        (('two', 'second', 'ii'), 2),
        (('three', 'third', 'iii'), 3),
        (('four', 'fourth', 'iv'), 4),
        (('five', 'fifth', 'v'), 5),
        (('six', 'sixth', 'vi'), 6),
        (('seven', 'seventh', 'vii'), 7),
        (('eight', 'eightth', 'viii'), 8),
        (('nine', 'nineth', 'ix'), 9),
        (('ten', 'tenth', 'x'), 10),
    ]
    for strs, num in word2num:
        name = re.sub(r'(?<=\b)({0})(?<=\b)'.format('|'.join(strs)),
                      str(num), name)

    name = re.sub(r'[:&-/]', ' ', name)
    words = filter(None, name.split())
    letters_remain = 3 if len(words) < 3 else len(words)
    slug = u''
    for w in words:
        w = w.strip('"\'')
        if not letters_remain:
            break
        add = w[-2:] if w.isdigit() else w[0]
        slug += add
        letters_remain -= len(add)
    if letters_remain:
        slug += w[1:letters_remain + 1]
    if slug in CardSet.objects.all().values_list('acronym', flat=True):
        slug = slug[:-1] + w[-1]

    return slug if re.match('[a-z0-9]+$', slug) else None


class CardSetsPipeline(BaseCardSetItemPipeline):
    @xact
    def _process_item(self, item, spider):
        name = item['name'].strip()
        # Return immediately if alias already exists
        if CardSetAlias.objects.filter(name=name).count():
            return

        # Get existing card set by name or create new one
        try:
            cs = CardSet.objects.get(name=name)
        except CardSet.DoesNotExist:
            # Save card set using form to pass all validation

            data = {
                'name': name,
                'acronym': generate_slug(name),
            }
            form = CardSetForm(data, instance=None)
            if not form.is_valid():
                raise InvalidData(form.errors.as_text())
            cs = form.save()

        # Save card set alias
        alias, _ = CardSetAlias.objects.get_or_create(
            name=item['name'], defaults={
                'card_set': cs, 'domain': spider.allowed_domains[0]})
        assert alias.card_set == cs


class InfoPipeline(BaseCardSetItemPipeline):
    def _process_item(self, item, spider):
        # TODO use CardSetForm

        cards = item.get('cards')
        released_at = item.get('released_at')

        if cards or released_at:
            cs = CardSetAlias.objects.get(name=item['name']).card_set

            if cards and cs.cards is None:
                cs.cards = int(cards)

            if released_at and re.match(r'\w+ \d+', released_at) and not cs.released_at:
                # Use first of given month, because particular day of
                # month is not provided
                cs.released_at = datetime.datetime.strptime(
                    '1 ' + released_at, '%d %B %Y')

            cs.save()
