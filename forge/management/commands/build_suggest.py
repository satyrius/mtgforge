from django.db import transaction, connection

from forge.models import FtsSuggest
from oracle.management.base import BaseCommand


class Command(BaseCommand):
    @transaction.commit_on_success
    def handle(self, *args, **options):
        cursor = connection.cursor()
        cursor.execute('DELETE FROM forge_ftssuggest')
        cursor.execute(r"""
            WITH words AS (
                SELECT unnest(regexp_split_to_array(concat_ws(' ', rules, type_line), E'\\s+')) AS word
                FROM oracle_cardface
            ), clean_words AS (
                SELECT replace(translate(lower(word), '():;.,"&?', ''), '''s', '') AS word
                FROM words
                WHERE word !~ '[{}\d\-\+]'
            )
            INSERT INTO forge_ftssuggest (term, weight)
            SELECT word, count(1)
            FROM clean_words
            GROUP BY word
            HAVING word != '' AND word ~ '^[a-z]{3,}$'
        """)
        self.notice(u'FTS suggest index was built, '
                    u'it contains {} words'.format(FtsSuggest.objects.count()))
