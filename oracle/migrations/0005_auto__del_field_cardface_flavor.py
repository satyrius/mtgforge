# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'CardFace.flavor'
        db.delete_column('oracle_cardface', 'flavor')


    def backwards(self, orm):
        # Adding field 'CardFace.flavor'
        db.add_column('oracle_cardface', 'flavor',
                      self.gf('contrib.fields.NullTextField')(null=True),
                      keep_default=False)


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'oracle.artist': {
            'Meta': {'object_name': 'Artist'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('contrib.fields.NullCharField', [], {'max_length': '255'})
        },
        'oracle.card': {
            'Meta': {'object_name': 'Card'},
            'faces_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('contrib.fields.NullCharField', [], {'max_length': '255'})
        },
        'oracle.cardface': {
            'Meta': {'object_name': 'CardFace'},
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oracle.Card']", 'blank': 'True'}),
            'cmc': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'color_identity': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'blank': 'True'}),
            'colors': ('arrayfields.fields.IntegerArrayField', [], {'default': '[]', 'blank': 'True'}),
            'fixed_power': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fixed_thoughtness': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loyality': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mana_cost': ('contrib.fields.NullCharField', [], {'max_length': '255', 'null': 'True'}),
            'name': ('contrib.fields.NullCharField', [], {'unique': 'True', 'max_length': '255'}),
            'place': ('contrib.fields.NullCharField', [], {'default': "'front'", 'max_length': '5', 'blank': 'True'}),
            'power': ('contrib.fields.NullCharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'rules': ('contrib.fields.NullTextField', [], {'null': 'True'}),
            'thoughtness': ('contrib.fields.NullCharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'type_line': ('contrib.fields.NullCharField', [], {'max_length': '255'}),
            'types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['oracle.CardType']", 'symmetrical': 'False'})
        },
        'oracle.cardimage': {
            'Meta': {'object_name': 'CardImage'},
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mvid': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'scan': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'oracle.cardl10n': {
            'Meta': {'unique_together': "(('card_face', 'card_release', 'language'),)", 'object_name': 'CardL10n'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oracle.Artist']"}),
            'card_face': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oracle.CardFace']", 'blank': 'True'}),
            'card_release': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oracle.CardRelease']", 'blank': 'True'}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'flavor': ('contrib.fields.NullTextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('contrib.fields.NullCharField', [], {'default': "'en'", 'max_length': '2', 'blank': 'True'}),
            'name': ('contrib.fields.NullCharField', [], {'max_length': '255'}),
            'rules': ('contrib.fields.NullTextField', [], {'null': 'True', 'blank': 'True'}),
            'scan': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'type_line': ('contrib.fields.NullCharField', [], {'max_length': '255'})
        },
        'oracle.cardrelease': {
            'Meta': {'object_name': 'CardRelease'},
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oracle.Card']"}),
            'card_number': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'card_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oracle.CardSet']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mvid': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'}),
            'rarity': ('contrib.fields.NullCharField', [], {'max_length': '1'})
        },
        'oracle.cardset': {
            'Meta': {'object_name': 'CardSet'},
            'acronym': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'cards': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_de': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_es': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_it': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_jp': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_ko': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_pt': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_tw': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'released_at': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'oracle.cardtype': {
            'Meta': {'object_name': 'CardType'},
            'category': ('contrib.fields.NullCharField', [], {'max_length': '9'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('contrib.fields.NullCharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'oracle.dataprovider': {
            'Meta': {'object_name': 'DataProvider'},
            'home': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'oracle.dataproviderpage': {
            'Meta': {'unique_together': "(('url_hash', 'class_name'),)", 'object_name': 'DataProviderPage'},
            'class_name': ('contrib.fields.NullCharField', [], {'max_length': '255'}),
            'content': ('contrib.fields.NullTextField', [], {}),
            'data_provider': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oracle.DataProvider']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('contrib.fields.NullCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'url_hash': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'oracle.datasource': {
            'Meta': {'unique_together': "(('content_type', 'object_id', 'url'), ('content_type', 'object_id', 'data_provider'))", 'object_name': 'DataSource'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'data_provider': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oracle.DataProvider']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['oracle']