import re


class Color(object):
    WHITE = 0b1
    BLUE = 0b10
    BLACK = 0b100
    RED = 0b1000
    GREEN = 0b10000
    COLORLESS = 0b100000

    MAP = dict(
        w=WHITE,
        u=BLUE,
        b=BLACK,
        r=RED,
        g=GREEN,
        c=COLORLESS,
    )

    def __init__(self, *args):
        i, c = 0, []
        reduce_to_identity = lambda c: reduce(lambda c1, c2: c1 | c2, c)
        if len(args):
            if isinstance(args[0], basestring):
                i, c = self.id_by_mana_cost(args[0])
            elif isinstance(args[0], (list, tuple)):
                c = args[0]
                i = reduce_to_identity(c)
            elif isinstance(args[0], int):
                c = map(int, args)
                i = reduce_to_identity(c)

        self.identity = i
        self.colors = c
        self.colors.sort()

    def id_by_mana_cost(self, mana_cost=None):
        identity = 0
        colors = []

        if mana_cost:
            costs = set(mana_cost.lower())
            has_colorless_mana = len(filter(lambda s: s.isdigit() or s == 'x', costs)) > 0
            allowed_symbols = self.MAP.keys()
            for s in filter(lambda s: s.isalpha() and s in allowed_symbols, costs):
                c = self.MAP[s]
                identity |= c
                colors.append(c)
            if not identity and has_colorless_mana:
                identity = self.COLORLESS
                colors = [self.COLORLESS]

        return identity, colors

    @property
    def names(self):
        return [name for name, id in self.MAP.items() if id in self.colors]


def parse_type_line(type_line):
    """Parse card face type line and return list of CardType objects. It also
    creates CardType if it does not exists"""
    if not type_line.strip():
        return []
    splited_types = map(lambda t: t.strip(), type_line.split('-', 2))

    split_types = lambda types: map(lambda t: t.capitalize(),
                                    filter(None, re.split(r'\s+', types)))
    main_types = split_types(splited_types[0])
    types = main_types[-1:]
    supertypes = main_types[:-1]
    subtypes = len(splited_types) > 1 and split_types(splited_types[1]) or []

    not_supertypes = {'Land', 'Artifact', 'Enchantment'}
    types.extend(list(set(supertypes) & not_supertypes))
    supertypes = list(set(supertypes) - not_supertypes)

    from oracle.models import CardType
    instances = []
    for types, cat in (
        (supertypes, CardType.SUPERTYPE),
        (types, CardType.TYPE),
        (subtypes, CardType.SUBTYPE),
    ):
        if not types:
            continue
        for name in types:
            t, _ = CardType.objects.get_or_create(
                name=name, defaults=dict(category=cat))
            instances.append(t)
    return instances
