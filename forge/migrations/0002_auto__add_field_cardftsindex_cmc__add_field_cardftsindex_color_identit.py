# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        db.execute("CREATE EXTENSION intarray")
        
        # Adding field 'CardFtsIndex.cmc'
        db.add_column('forge_cardftsindex', 'cmc', self.gf('django.db.models.fields.IntegerField')(null=True), keep_default=False)

        # Adding field 'CardFtsIndex.color_identity'
        db.add_column('forge_cardftsindex', 'color_identity', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        db.execute("ALTER TABLE forge_cardftsindex ADD COLUMN sets int[]")
        db.execute("""
            CREATE INDEX forge_cardftsindex_sets_idx
            ON forge_cardftsindex 
            USING GIST (sets gist__int_ops)
        """)


    def backwards(self, orm):
        
        # Deleting field 'CardFtsIndex.cmc'
        db.delete_column('forge_cardftsindex', 'cmc')

        # Deleting field 'CardFtsIndex.color_identity'
        db.delete_column('forge_cardftsindex', 'color_identity')


    models = {
        'forge.cardftsindex': {
            'Meta': {'object_name': 'CardFtsIndex'},
            'card': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fts'", 'to': "orm['oracle.Card']"}),
            'cmc': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'color_identity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'oracle.card': {
            'Meta': {'object_name': 'Card'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('contrib.fields.NullCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['forge']
