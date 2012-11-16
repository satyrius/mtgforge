import re
from oracle.management.base import BaseCommand
from oracle.models import CardFace, CardType


sep = re.compile(r'\s+')

class Command(BaseCommand):
    def writeln_type(self, card_face, card_type):
        self.writeln(u'{0}: {1} {2}'.format(card_face.name, card_type.name, card_type.category))

    def parse_types(self, card_face, types, category):
        if not types:
            return
        for t_name in isinstance(types, basestring) and sep.split(types) or types:
            t = CardType.objects.get_or_create(name=t_name, category=category)[0]
            card_face.types.add(t)
            self.writeln_type(card_face, t)

    def handle(self, *args, **options):
        for face in CardFace.objects.all():
            face.types.clear()
            splited_types = map(lambda t: t.strip(), face.type_line.split('-', 2))

            main_types = sep.split(splited_types[0])
            types = main_types[-1:]
            supertypes = main_types[:-1]

            for exclude in ['Land', 'Artifact', 'Enchantment']:
                if exclude in supertypes:
                    types.append(exclude)
                    supertypes = filter(lambda t: t != exclude, supertypes)

            self.parse_types(face, supertypes, CardType.SUBTYPE)
            self.parse_types(face, types, CardType.TYPE)

            if len(splited_types) > 1:
                self.parse_types(face, splited_types[1], CardType.SUBTYPE)

            face.save()
