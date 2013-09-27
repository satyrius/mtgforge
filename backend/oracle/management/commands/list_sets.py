from optparse import make_option

from contrib.commands import BaseCommand
from oracle.models import CardSet


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-s', '--sort', dest='sort', default='name',
                    help='Sorting method: name, acronym, release '
                         '[default %default]'),
    )

    def handle(self, *args, **options):
        objects = CardSet.objects.all()
        sorting = dict(name=['name'], acronym=['acronym'], release=['released_at', 'name'])
        sort = sorting.get(options['sort'], sorting['name'])
        for cs in objects.order_by(*sort):
            self.writeln('{:<6} {}'.format(cs.acronym, cs.name))
