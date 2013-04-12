import re

from django.conf import settings
from django.db import connection
from functools import wraps

from oracle.models import CardSet, Color, CardFace


def valueble(func=None, callback=None, assert_list=False):
    if func:
        @wraps(func)
        def wrapper(self, value):
            if callback:
                value = callback(value)
            if assert_list:
                assert isinstance(value, (list, tuple))
            if value:
                r = func(self, value)
                return r is None and self or r
            else:
                return self
        return wrapper
    else:
        def decorator(func):
            return valueble(func, callback)
        return decorator


class FtsQuery(object):
    FTS_TEMPLATE = """
        SELECT DISTINCT ON ({rank}, r.card_id)
            f.*,
            img.*,
            thumb.file AS thumb,
            {rank} AS rank
        FROM forge_cardftsindex AS i
        JOIN oracle_cardface AS f ON f.id = i.card_face_id
        JOIN oracle_cardrelease AS r ON r.card_id = f.card_id
        JOIN oracle_cardset AS cs ON cs.id = r.card_set_id
        JOIN oracle_cardimage AS img ON img.id = r.art_id
        LEFT JOIN oracle_cardimagethumb AS thumb
            ON thumb.original_id = img.id
            AND format = %(thumb_fmt)s
        WHERE
            TRUE
            {search_filter}
            {set_filter}
            {rarity_filter}
            {color_filter}
            {type_filter}
            {cmc_filter}
        ORDER BY {rank} DESC, r.card_id, cs.released_at DESC
    """

    COUNT_TEMPLATE = "SELECT COUNT(1) FROM ({query}) AS t".format(
        query=FTS_TEMPLATE)

    def __init__(self, cursor=None):
        self.cursor = cursor
        self.reset()

    def get_cursor(self):
        if not self.cursor:
            self.cursor = connection.cursor()
        return self.cursor

    def reset(self):
        self.params = {'thumb_fmt': settings.CARD_IMAGE_SERP_THUMB}
        self.filters = {
            'search_filter': '',
            'set_filter': '',
            'rarity_filter': '',
            'color_filter': '',
            'type_filter': '',
            'cmc_filter': '',
            'rank': '1',
        }
        self.meta = {}

    def add_term(self, **terms):
        for term, value in terms.items():
            add = getattr(self, u'add_{}'.format(term))
            add(value)
        return self

    @valueble(callback=lambda v: v and v.strip(' \n\t'))
    def add_q(self, value):
        # Check similatity and save both queries to the meta
        search, original = similarity_check(self.get_cursor(), value)
        self.meta['query'] = search
        self.meta['original_query'] = original

        # Split query by space and build ts_vector filter
        search = [u'%s:*' % s for s in search.split(' ')]
        self.params['q'] = u' & '.join(search)
        self.filters['search_filter'] = 'AND i.fts @@ to_tsquery(%(q)s)'
        self.filters['rank'] = 'ts_rank_cd(array[0.1,0.5,1,0.8], i.fts, to_tsquery(%(q)s), 4)'

    @valueble(assert_list=True)
    def add_set(self, value):
        set_ids = CardSet.objects.filter(
            acronym__in=value).values_list('id', flat=True)
        self.meta['sets_filtered'] = len(set_ids)
        self.filters['set_filter'] = "AND i.sets @@ '{0}'::query_int".format(
            '|'.join(map(str, set_ids)))

    @valueble(assert_list=True)
    def add_rarity(self, value):
        self.filters['rarity_filter'] = 'AND i.fts @@ to_tsquery(%(rarity)s)'
        self.params['rarity'] = u' | '.join(
            [u'%s:B*' % q.strip(' \n\t') for q in value])

    @valueble(assert_list=True)
    def add_color(self, value):
        color = value[:]
        if 'a' in color:
            color.remove('a')
            operator = u' & '
        else:
            operator = u' | '

        identity_query = [str(Color.MAP[c]) for c in color]
        identity_query = u"'%s'::query_int" % operator.join(identity_query)
        self.filters['color_filter'] = u'AND i.color_identity_idx @@ {0}'.format(
            identity_query)

    @valueble(assert_list=True)
    def add_type(self, value):
        type_query = [u'%s:B*' % q.strip(' \n\t') for q in value]
        self.filters['type_filter'] = 'AND i.fts @@ to_tsquery(%(type)s)'
        self.params['type'] = u' | '.join(type_query)

    @valueble(assert_list=True)
    def add_cmc(self, value):
        cmc = map(int, value)
        cmc_filter = 'AND (i.cmc = ANY(%(cmc)s){higher_cost})'
        higher_cost = 7 in cmc and ' OR i.cmc > 7' or ''
        self.filters['cmc_filter'] = cmc_filter.format(higher_cost=higher_cost)
        self.params['cmc'] = cmc

    def execute_count(self):
        cursor = self.get_cursor()
        query = self.COUNT_TEMPLATE.format(**self.filters)
        cursor.execute(query, self.params)
        return cursor.fetchone()[0]

    def execute(self, limit, offset=0):
        query = self.FTS_TEMPLATE + """
            limit %(limit)s
            offset %(offset)s
        """
        params = self.params.copy()
        params.update(limit=limit, offset=offset)
        return CardFace.objects.raw(query.format(**self.filters), params)


def similarity_check(cursor, query):
    original = query
    query = re.split('[^\w]', query.lower(), flags=re.I)
    cursor.execute("""
        SELECT DISTINCT ON (sim.keyword) src.kw, sim.keyword
        FROM (
            SELECT UNNEST(ARRAY[%s]) kw
        ) src, forge_cardsimilarity sim
        WHERE
            NOT EXISTS(
                SELECT id
                FROM forge_cardsimilarity
                WHERE keyword = src.kw
            )
            AND sim.keyword %% src.kw
        ORDER BY sim.keyword, similarity(sim.keyword, src.kw)
    """, [query])
    modifications = cursor.fetchall()
    modified = original
    for source, changed in modifications:
        modified = modified.replace(source, changed)

    return modified, original
