# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DataProvider'
        db.create_table('oracle_dataprovider', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('contrib.fields.NullCharField')(unique=True, max_length=20)),
            ('title', self.gf('contrib.fields.NullCharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('oracle', ['DataProvider'])


    def backwards(self, orm):
        
        # Deleting model 'DataProvider'
        db.delete_table('oracle_dataprovider')


    models = {
        'oracle.cardset': {
            'Meta': {'object_name': 'CardSet'},
            'acronym': ('contrib.fields.NullCharField', [], {'unique': 'True', 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('contrib.fields.NullCharField', [], {'unique': 'True', 'max_length': '255'}),
            'name_en': ('contrib.fields.NullCharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('contrib.fields.NullCharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'oracle.dataprovider': {
            'Meta': {'object_name': 'DataProvider'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('contrib.fields.NullCharField', [], {'unique': 'True', 'max_length': '20'}),
            'title': ('contrib.fields.NullCharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['oracle']
