# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DataProvider'
        db.create_table('oracle_dataprovider', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('home', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'crawler', ['DataProvider'])

        # Adding model 'DataSource'
        db.create_table('oracle_datasource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('data_provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crawler.DataProvider'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'crawler', ['DataSource'])

        # Adding unique constraint on 'DataSource', fields ['content_type', 'object_id', 'url']
        db.create_unique('oracle_datasource', ['content_type_id', 'object_id', 'url'])

        # Adding unique constraint on 'DataSource', fields ['content_type', 'object_id', 'data_provider']
        db.create_unique('oracle_datasource', ['content_type_id', 'object_id', 'data_provider_id'])

        # Adding model 'DataProviderPage'
        db.create_table('oracle_dataproviderpage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('url_hash', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('data_provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crawler.DataProvider'], null=True, blank=True)),
            ('content', self.gf('contrib.fields.NullTextField')()),
            ('class_name', self.gf('contrib.fields.NullCharField')(max_length=255)),
            ('name', self.gf('contrib.fields.NullCharField')(max_length=255, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal(u'crawler', ['DataProviderPage'])

        # Adding unique constraint on 'DataProviderPage', fields ['url_hash', 'class_name']
        db.create_unique('oracle_dataproviderpage', ['url_hash', 'class_name'])


    def backwards(self, orm):
        # Removing unique constraint on 'DataProviderPage', fields ['url_hash', 'class_name']
        db.delete_unique('oracle_dataproviderpage', ['url_hash', 'class_name'])

        # Removing unique constraint on 'DataSource', fields ['content_type', 'object_id', 'data_provider']
        db.delete_unique('oracle_datasource', ['content_type_id', 'object_id', 'data_provider_id'])

        # Removing unique constraint on 'DataSource', fields ['content_type', 'object_id', 'url']
        db.delete_unique('oracle_datasource', ['content_type_id', 'object_id', 'url'])

        # Deleting model 'DataProvider'
        db.delete_table('oracle_dataprovider')

        # Deleting model 'DataSource'
        db.delete_table('oracle_datasource')

        # Deleting model 'DataProviderPage'
        db.delete_table('oracle_dataproviderpage')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'crawler.dataprovider': {
            'Meta': {'object_name': 'DataProvider', 'db_table': "'oracle_dataprovider'"},
            'home': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'crawler.dataproviderpage': {
            'Meta': {'unique_together': "(('url_hash', 'class_name'),)", 'object_name': 'DataProviderPage', 'db_table': "'oracle_dataproviderpage'"},
            'class_name': ('contrib.fields.NullCharField', [], {'max_length': '255'}),
            'content': ('contrib.fields.NullTextField', [], {}),
            'data_provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crawler.DataProvider']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('contrib.fields.NullCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'url_hash': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'crawler.datasource': {
            'Meta': {'unique_together': "(('content_type', 'object_id', 'url'), ('content_type', 'object_id', 'data_provider'))", 'object_name': 'DataSource', 'db_table': "'oracle_datasource'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'data_provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crawler.DataProvider']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['crawler']