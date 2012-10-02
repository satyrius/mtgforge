from optparse import make_option
from django.core.management import base


class BaseCommand(base.BaseCommand):
    option_list = base.BaseCommand.option_list + (
        make_option('-d', '--dry-run',
            action='store_true',
            dest='dry_run',
            default=False,
            help='Do not save fetched data'),
        )

    def writeln(self, message):
        message = u'{0}\n'.format(message)
        self.stdout.write(message)

    def notice(self, message):
        colorized_message = self.style.SQL_COLTYPE(message)
        self.writeln(colorized_message)

    def error(self, message):
        colorized_message = self.style.NOTICE(u'{0}\n'.format(message))
        self.stderr.write(base.smart_str(colorized_message))
