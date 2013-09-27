from django.core.management import base
from django.utils.encoding import smart_text


class BaseCommand(base.BaseCommand):
    def unicode(self, message):
        if isinstance(message, unicode):
            return message
        return unicode(str(message), 'utf8')

    def writeln(self, message):
        message = u'{0}\n'.format(self.unicode(message))
        self.stdout.write(message)

    def notice(self, message):
        colorized_message = self.style.SQL_COLTYPE(message)
        self.writeln(colorized_message)

    def error(self, message):
        colorized_message = self.style.NOTICE(
            u'{0}\n'.format(self.unicode(message)))
        self.stderr.write(smart_text(colorized_message))
