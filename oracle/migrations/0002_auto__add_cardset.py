# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'CardSet'
        db.create_table('oracle_cardset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('contrib.fields.NullCharField')(unique=True, max_length=255)),
            ('acronym', self.gf('contrib.fields.NullCharField')(unique=True, max_length=10)),
        ))
        db.send_create_signal('oracle', ['CardSet'])


    def backwards(self, orm):
        
        # Deleting model 'CardSet'
        db.delete_table('oracle_cardset')


    models = {
        'oracle.cardset': {
            'Meta': {'object_name': 'CardSet'},
            'acronym': ('contrib.fields.NullCharField', [], {'unique': 'True', 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('contrib.fields.NullCharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['oracle']
