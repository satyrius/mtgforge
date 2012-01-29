# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DataSource'
        db.create_table('oracle_datasource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('contrib.fields.NullURLField')(max_length=200)),
            ('data_provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oracle.DataProvider'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('oracle', ['DataSource'])

        # Adding unique constraint on 'DataSource', fields ['content_type', 'object_id', 'url']
        db.create_unique('oracle_datasource', ['content_type_id', 'object_id', 'url'])

        # Adding unique constraint on 'DataSource', fields ['content_type', 'object_id', 'data_provider']
        db.create_unique('oracle_datasource', ['content_type_id', 'object_id', 'data_provider_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'DataSource', fields ['content_type', 'object_id', 'data_provider']
        db.delete_unique('oracle_datasource', ['content_type_id', 'object_id', 'data_provider_id'])

        # Removing unique constraint on 'DataSource', fields ['content_type', 'object_id', 'url']
        db.delete_unique('oracle_datasource', ['content_type_id', 'object_id', 'url'])

        # Deleting model 'DataSource'
        db.delete_table('oracle_datasource')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'oracle.cardset': {
            'Meta': {'object_name': 'CardSet'},
            'acronym': ('contrib.fields.NullCharField', [], {'unique': 'True', 'max_length': '10'}),
            'cards': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('contrib.fields.NullCharField', [], {'unique': 'True', 'max_length': '255'}),
            'name_en': ('contrib.fields.NullCharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('contrib.fields.NullCharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'released_at': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'oracle.dataprovider': {
            'Meta': {'object_name': 'DataProvider'},
            'home': ('contrib.fields.NullURLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('contrib.fields.NullCharField', [], {'unique': 'True', 'max_length': '20'}),
            'title': ('contrib.fields.NullCharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'oracle.datasource': {
            'Meta': {'unique_together': "(('content_type', 'object_id', 'url'), ('content_type', 'object_id', 'data_provider'))", 'object_name': 'DataSource'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'data_provider': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oracle.DataProvider']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'url': ('contrib.fields.NullURLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['oracle']
