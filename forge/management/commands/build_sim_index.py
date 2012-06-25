import re

from django.core.management.base import BaseCommand
from django.db import transaction, connection

from forge.models import CardSimilarity
from oracle.models import CardL10n

def exists(cur, keyword):
    cur.execute("""
        SELECT count(*) FROM forge_cardsimilarity 
        WHERE keyword = %s
    """, [keyword])
    return cur.fetchone()[0]

class Command(BaseCommand):

    @transaction.commit_on_success    
    def handle(self, *args, **options):
        
        cursor = connection.cursor()       
        for card in CardL10n.objects.all():
            keywords = []
            if card.rules:
                keywords = re.split('[^\w]', card.rules, flags=re.IGNORECASE)

            keywords += re.split('[^\w]', card.name, flags=re.IGNORECASE)
            keywords += re.split('[^\w]', card.type_line, flags=re.IGNORECASE)
            for keyword in keywords:
                if not keyword: continue
                keyword = keyword.lower()
                if not exists(cursor, keyword):
                    CardSimilarity(keyword=keyword).save()
                    
            
        

        
        
