# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'CardFtsIndex'
        db.create_table('forge_cardftsindex', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fts', to=orm['oracle.Card'])),
        ))
        db.execute('ALTER TABLE forge_cardftsindex ADD COLUMN fts tsvector')
        db.execute('CREATE INDEX forge_cardftsindex_fts_idx ON forge_cardftsindex USING gin(fts)')
        db.execute('DROP FUNCTION oracle_card_colors(int)')
        db.send_create_signal('forge', ['CardFtsIndex'])


    def backwards(self, orm):
        
        # Deleting model 'CardFtsIndex'
        db.delete_table('forge_cardftsindex')


    models = {
        'forge.cardftsindex': {
            'Meta': {'object_name': 'CardFtsIndex'},
            'card': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fts'", 'to': "orm['oracle.Card']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'oracle.card': {
            'Meta': {'object_name': 'Card'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('contrib.fields.NullCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['forge']
