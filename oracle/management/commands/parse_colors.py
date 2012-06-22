from oracle.management.base import BaseCommand
from oracle.models import CardFace, Color


class Command(BaseCommand):
    def handle(self, *args, **options):
        for face in CardFace.objects.all():
            face.color_identity = Color(face.mana_cost).identity
            self.writeln(u'"{0}" mana cost is {2} and color identity is {1}'.format(
                face.name, face.color_identity, face.mana_cost))
            face.save()
