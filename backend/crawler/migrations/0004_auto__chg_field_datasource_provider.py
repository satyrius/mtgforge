# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'DataSource.provider'
        db.alter_column('oracle_datasource', 'provider', self.gf('contrib.fields.NullCharField')(default=None, max_length=10))

    def backwards(self, orm):

        # Changing field 'DataSource.provider'
        db.alter_column('oracle_datasource', 'provider', self.gf('contrib.fields.NullCharField')(max_length=10, null=True))

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
            'provider': ('contrib.fields.NullCharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'url_hash': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'crawler.datasource': {
            'Meta': {'unique_together': "(('content_type', 'object_id', 'url'), ('content_type', 'object_id', 'data_provider'), ('content_type', 'object_id', 'provider'))", 'object_name': 'DataSource', 'db_table': "'oracle_datasource'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'data_provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crawler.DataProvider']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'provider': ('contrib.fields.NullCharField', [], {'max_length': '10'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['crawler']