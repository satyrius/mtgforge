# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'DataProvider.home'
        db.add_column('oracle_dataprovider', 'home', self.gf('contrib.fields.NullURLField')(default='http://example.com', max_length=200), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'DataProvider.home'
        db.delete_column('oracle_dataprovider', 'home')


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
            'home': ('contrib.fields.NullURLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('contrib.fields.NullCharField', [], {'unique': 'True', 'max_length': '20'}),
            'title': ('contrib.fields.NullCharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['oracle']
