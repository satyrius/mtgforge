from oracle.management.base import BaseCommand
from oracle.models import CardFace, Color


class Command(BaseCommand):
    def handle(self, *args, **options):
        for face in CardFace.objects.all():
            c = Color(face.mana_cost)
            face.color_identity = c.identity
            face.colors = c.colors
            self.writeln(u'"{0}" mana cost is {2} and color identity is {1}'.format(
                face.name, face.color_identity, face.mana_cost))
            face.save()
