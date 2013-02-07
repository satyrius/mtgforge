from oracle.management.base import BaseCommand
from oracle.models import Card, CardFace
from django.db.models import Count


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Get gards with many faces (splited/fliped/double-faced)
        splited = {'in', 'ap', 'uh', 'di', 'pc', 'pch', 'arc', 'ddh'}
        fliped = {'chk', 'bok', 'sok'}
        double_faced = {'isd', 'dka'}
        for card in Card.objects.annotate(num_of_faces=Count('cardface')).filter(num_of_faces__gt=1):
            card.faces_count = card.num_of_faces
            card.save()
            cs = {r.card_set.acronym for r in card.cardrelease_set.all()}
            # All splited card faces mark with type 'flip'
            if cs & splited:
                for face in card.cardface_set.all():
                    self.writeln(u'"{0}" is treated as SPLIT face'.format(face.name))
                    face.place = CardFace.SPLIT
                    face.save()
                continue
            try:
                face = card.cardface_set.get(mana_cost=None)
            except CardFace.DoesNotExist:
                self.error(u'There is not face without mana cost for "{0}", '
                           'cannot choose back/splited face'.format(card.name))
                continue

            if cs & fliped:
                self.writeln(u'"{0}" is treated as FLIPED face'.format(face.name))
                face.place = CardFace.FLIP
            elif cs & double_faced:
                self.writeln(u'"{0}" is treated as BACK face'.format(face.name))
                face.place = CardFace.BACK
            face.save()
