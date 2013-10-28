import re
from fabric.api import prompt


def are_you_sure(ask_message, default='no'):
    yes = r'y(e(p|a[h]*)?)?|true|1'
    no = r'n(o(pe)?)?|false|0'

    def yes_no(value):
        value = value.strip().lower()
        if not re.match(r'^%s|%s$' % (yes, no), value):
            raise Exception('It is a yes/no question.')
        return bool(re.match(yes, value))

    return prompt(u'%s Are you sure? [yes/no]' % ask_message, default=default,
                  validate=yes_no)
