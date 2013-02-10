from django.core.management.base import BaseCommand
from django.db import connection, transaction

from oracle.models import Color


class Command(BaseCommand):

    @transaction.commit_on_success
    def handle(self, *args, **options):

        statements = [
            """--Cleanup fts index table
            DELETE FROM forge_cardftsindex
            """,

            """--Populate fts with empty index
            INSERT INTO forge_cardftsindex (card_id, card_face_id, fts, color_identity, color_identity_idx)
            SELECT card_id, id, ''::tsvector, 0, ARRAY[]::int[] FROM oracle_cardface
            """,

            """--Populate tsvector from names, type_lines and rules
            UPDATE forge_cardftsindex SET fts = fts
                || setweight(to_tsvector(n.names), 'A')
                || setweight(to_tsvector(n.types), 'B')
                || setweight(to_tsvector(n.rules), 'C')
            FROM (
                SELECT f.id,
                    array_to_string(array_agg(COALESCE(l.name, f.name)), ' ') AS names,
                    array_to_string(array_agg(COALESCE(l.type_line, f.type_line)), ' ') AS types,
                    array_to_string(array_agg(COALESCE(l.rules, f.rules)), ' ') AS rules
                FROM oracle_cardface AS f
                LEFT JOIN oracle_cardl10n AS l ON (l.card_face_id = f.id)
                GROUP BY f.id
            ) AS n
            WHERE n.id = card_face_id
            """,

            """--Poulate table with colors
            UPDATE forge_cardftsindex set color_identity = f.color_identity
            FROM oracle_cardface f
            WHERE forge_cardftsindex.card_face_id = f.id
            """,

            """--Populate tsvector from colors
            UPDATE forge_cardftsindex SET fts = fts ||
                setweight(to_tsvector(array_to_string(
                    ARRAY[
                        (ARRAY[{colors}])[1 + ((color_identity & {Color.WHITE}     ) >> 0)*1],
                        (ARRAY[{colors}])[1 + ((color_identity & {Color.BLUE}      ) >> 1)*2],
                        (ARRAY[{colors}])[1 + ((color_identity & {Color.BLACK}     ) >> 2)*3],
                        (ARRAY[{colors}])[1 + ((color_identity & {Color.RED}       ) >> 3)*4],
                        (ARRAY[{colors}])[1 + ((color_identity & {Color.GREEN}     ) >> 4)*5],
                        (ARRAY[{colors}])[1 + ((color_identity & {Color.COLORLESS} ) >> 5)*6]
                    ], ' '
                )), 'B')
            """.format(colors="'', 'white', 'blue', 'black', 'red', 'green', 'colorless'", Color=Color),

            """--Create color index for white
            UPDATE forge_cardftsindex
            SET color_identity_idx = array_append(color_identity_idx, 1)
            WHERE color_identity & 1 > 0
            """,

            """--Create color index for  blue
            UPDATE forge_cardftsindex
            SET color_identity_idx = array_append(color_identity_idx, 2)
            WHERE color_identity & 2 > 0
            """,

            """--Create color index for black
            UPDATE forge_cardftsindex
            SET color_identity_idx = array_append(color_identity_idx, 4)
            WHERE color_identity & 4 > 0
            """,

            """--Create color index for red
            UPDATE forge_cardftsindex
            SET color_identity_idx = array_append(color_identity_idx, 8)
            WHERE color_identity & 8 > 0
            """,

            """--Create color index for green
            UPDATE forge_cardftsindex
            SET color_identity_idx = array_append(color_identity_idx, 16)
            WHERE color_identity & 16 > 0
            """,

            """--Create color index for colorless
            UPDATE forge_cardftsindex
            SET color_identity_idx = array_append(color_identity_idx, 32)
            WHERE color_identity & 32 > 0
            """,

            """--Populate table with converted mana cost (cmc)
            UPDATE forge_cardftsindex SET cmc = f.cmc
            FROM oracle_cardface AS f
            WHERE forge_cardftsindex.card_face_id = f.id
            """,

            """--Populate tsvector from converted mana cost
            UPDATE forge_cardftsindex SET fts = fts ||
            CASE
                WHEN cmc <= 1
                THEN setweight(to_tsvector('cheap'), 'C')
                WHEN cmc in (2, 3)
                THEN setweight(to_tsvector('cheap'), 'D')
                ELSE to_tsvector('')
            END
            WHERE cmc IS NOT NULL
            """,

            """--Populate table with releases
            UPDATE forge_cardftsindex set sets = (
                SELECT array_agg(r.card_set_id)
                FROM oracle_cardrelease r
                WHERE r.card_id = forge_cardftsindex.card_id
            )
            """,
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
