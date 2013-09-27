from optparse import make_option
from contrib import commands


class BaseCommand(commands.BaseCommand):
    option_list = commands.BaseCommand.option_list + (
        make_option(
            '-d', '--dry-run',
            action='store_true',
            dest='dry_run',
            default=False,
            help='Do not save fetched data'),
    )
