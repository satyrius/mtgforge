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
