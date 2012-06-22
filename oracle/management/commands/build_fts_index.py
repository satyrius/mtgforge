from django.core.management.base import BaseCommand
from django.db import connection, transaction

class Command(BaseCommand):
    
    @transaction.commit_on_success
    def handle(self, *args, **options):
        
        statements = [
            """--Cleanup fts index table
            DELETE FROM oracle_cardftsindex
            """,

            """--Populate fts with empty index
            INSERT INTO oracle_cardftsindex (card_id, fts)
            SELECT id, ''::tsvector FROM oracle_card
            """,

            """--Populate tsvector from names, type_lines and rules
            UPDATE oracle_cardftsindex SET fts = fts 
                || setweight(to_tsvector(n.names), 'A')
                || setweight(to_tsvector(n.types), 'B')
                || setweight(to_tsvector(n.rules), 'B')
            FROM (
                SELECT c.id as id, 
                    array_to_string(array_agg(t.name), ' ') as names,
                    array_to_string(array_agg(t.type_line), ' ') as types,
                    array_to_string(array_agg(t.rules), ' ') as rules
                FROM oracle_card c 
                JOIN oracle_cardface f ON (c.id = f.card_id) 
                JOIN oracle_cardl10n t on (t.card_face_id = f.id) 
                GROUP BY c.id
            ) AS n
            WHERE n.id = card_id
            """,

            """--Populate tsvector from colors
            UPDATE oracle_cardftsindex SET fts = fts || 
                setweight(to_tsvector(array_to_string(
                    oracle_card_colors(card_id), ' '
                )), 'B')
            """,

            """--Populate tsvector from converted mana cost
            UPDATE oracle_cardftsindex SET fts = fts || 
            CASE 
                WHEN n.cmc <= 1 
                THEN setweight(to_tsvector('cheap'), 'B')
                WHEN n.cmc in (2, 3) 
                THEN setweight(to_tsvector('cheap'), 'C')
                ELSE to_tsvector('')
            END
            FROM oracle_cardface n
            WHERE n.card_id = oracle_cardftsindex.card_id AND cmc IS NOT NULL
            """
        ]
        
        sql_no = 1
        notices = 0
        cursor = connection.cursor()
        for sql in statements:
            debug_msg = sql.split("\n")[0].strip(" -")
            print "Executing %d/%d: %s" % (sql_no, len(statements), debug_msg)
            sql_no += 1

            cursor.execute(sql)

            if connection.connection.notices[notices:]:
                print "".join(connection.connection.notices[notices:]).strip(" \n\t")
                notices += len(connection.connection.notices[notices:])





