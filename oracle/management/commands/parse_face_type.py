from oracle.management.base import BaseCommand
from oracle.models import Card, CardFace
from django.db.models import Count


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Get gards with many faces (splited/fliped/double-faced)
        splited = ['in', 'ap', 'uh', 'di', 'pc', 'pch', 'arc', 'ddh']
        fliped = ['chk', 'bok', 'sok']
        double_faced = ['isd', 'dka']
        for card in Card.objects.annotate(faces_count=Count('cardface')).filter(faces_count__gt=1):
            cs = card.cardrelease_set.all()[0].card_set.acronym
            # All splited card faces mark with type 'flip'
            if cs in splited:
                for face in card.cardface_set.all():
                    self.writeln(u'"{0}" is treated as SPLIT face'.format(face.name))
                    face.place = CardFace.SPLIT
                    face.save()
                continue
            face = card.cardface_set.get(mana_cost=None)
            if cs in fliped:
                self.writeln(u'"{0}" is treated as FLIPED face'.format(face.name))
                face.place = CardFace.FLIP
            elif cs in double_faced:
                self.writeln(u'"{0}" is treated as BACK face'.format(face.name))
                face.place = CardFace.BACK
            face.save()
