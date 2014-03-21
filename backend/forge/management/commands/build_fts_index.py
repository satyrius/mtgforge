from django.core.management.base import BaseCommand
from django.db import connection, transaction

from oracle.models import Color


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        silent = options['verbosity'] == 0

        # A - very important card parts (e.g. types), higher SERP
        #     position if matched
        # B - important info, usually used for filtering (e.g. color, rarity)
        # C - common info (e.g. card name, rules)
        # D - some noise

        statements = [
            """--Cleanup fts index table
            DELETE FROM forge_cardftsindex
            """,

            """--Populate fts with empty index
            INSERT INTO forge_cardftsindex (
                card_id, card_face_id, fts, color_identity,
                color_identity_idx, face_order)
            SELECT f.card_id, f.id, ''::tsvector, 0, ARRAY[]::int[], CASE
                WHEN f.place = '{CardFace.FRONT}' THEN 0
                WHEN f.place = '{CardFace.SPLIT}' THEN 1
                ELSE 2
            END
            FROM oracle_cardface AS f
            JOIN oracle_cardrelease AS r ON r.card_id = f.card_id
            JOIN oracle_cardset AS cs ON cs.id = r.card_set_id
            WHERE cs.is_published
            GROUP BY f.card_id, f.id, f.place
            """,

            # NAME AND RULES

            r"""--Populate tsvector from names, type_lines and rules
            UPDATE forge_cardftsindex SET fts = fts
                || setweight(to_tsvector(n.types), 'A')
                || setweight(to_tsvector(n.names), 'C')
                || setweight(to_tsvector(n.rules), 'C')
            FROM (
                SELECT f.id,
                    array_to_string(array_agg(COALESCE(l.name, f.name)), ' ') AS names,
                    array_to_string(array_agg(COALESCE(l.type_line, f.type_line)), ' ') AS types,
                    array_to_string(array_agg(regexp_replace(COALESCE(l.rules, f.rules), '\([^)]+\)', '')), ' ') AS rules
                FROM oracle_cardface AS f
                LEFT JOIN oracle_cardl10n AS l ON (l.card_face_id = f.id)
                GROUP BY f.id
            ) AS n
            WHERE n.id = card_face_id
            """,

            # COLOR

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

            # MANA COST

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

            # RELEASE AT CARD SET AND RARITY

            """--Populate table with releases
            UPDATE forge_cardftsindex set sets = (
                SELECT array_agg(r.card_set_id)
                FROM oracle_cardrelease r
                JOIN oracle_cardset AS cs ON cs.id = r.card_set_id
                WHERE TRUE
                    AND cs.is_published
                    AND r.card_id = forge_cardftsindex.card_id
            )
            """,

            """--Card set names
            UPDATE forge_cardftsindex SET fts = fts
                || setweight(to_tsvector(
                    array_to_string((
                        SELECT array_agg(cs.name)
                        FROM oracle_cardset AS cs
                        WHERE cs.id = ANY(sets)
                    ), '')
                ), 'B')

            """,

            """--Create rarity index
            UPDATE forge_cardftsindex SET fts = fts
                || setweight(to_tsvector(array_to_string(n.rarity, '')), 'B')
            FROM (
                SELECT c.id, array_agg(DISTINCT CASE
                    WHEN r.rarity = 'c' THEN 'common'
                    WHEN r.rarity = 'u' THEN 'uncommon'
                    WHEN r.rarity = 'r' THEN 'rare'
                    WHEN r.rarity = 'm' THEN 'mythic'
                END) AS rarity
                FROM oracle_card AS c
                JOIN oracle_cardrelease AS r ON r.card_id = c.id
                JOIN oracle_cardset AS cs ON cs.id = r.card_set_id
                WHERE cs.is_published
                GROUP BY c.id
            ) AS n
            WHERE n.id = card_id
            """,
        ]

        sql_no = 1
        notices = 0
        cursor = connection.cursor()
        for sql in statements:
            if not silent:
                debug_msg = sql.split("\n")[0].strip(" -")
                print "Executing %d/%d: %s" % (sql_no, len(statements), debug_msg)
            sql_no += 1

            cursor.execute(sql)

            if connection.connection.notices[notices:]:
                print "".join(connection.connection.notices[notices:]).strip(" \n\t")
                notices += len(connection.connection.notices[notices:])
