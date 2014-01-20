# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CardSet.created_at'
        db.add_column(u'oracle_cardset', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime.utcnow(), blank=True),
                      keep_default=False)

        # Adding field 'CardSet.updated_at'
        db.add_column(u'oracle_cardset', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime.utcnow(), blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'CardSet.created_at'
        db.delete_column(u'oracle_cardset', 'created_at')

        # Deleting field 'CardSet.updated_at'
        db.delete_column(u'oracle_cardset', 'updated_at')

    models = {
        u'oracle.artist': {
            'Meta': {'object_name': 'Artist'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('contrib.fields.NullCharField', [], {'max_length': '255'})
        },
        u'oracle.card': {
            'Meta': {'object_name': 'Card'},
            'faces_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('contrib.fields.NullCharField', [], {'max_length': '255'})
        },
        u'oracle.cardface': {
            'Meta': {'object_name': 'CardFace'},
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oracle.Card']", 'blank': 'True'}),
            'cmc': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'color_identity': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'blank': 'True'}),
            'colors': ('arrayfields.fields.IntegerArrayField', [], {'default': '[]', 'blank': 'True'}),
            'fixed_power': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fixed_thoughtness': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loyality': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mana_cost': ('contrib.fields.NullCharField', [], {'max_length': '255', 'null': 'True'}),
            'name': ('contrib.fields.NullCharField', [], {'unique': 'True', 'max_length': '255'}),
            'place': ('contrib.fields.NullCharField', [], {'default': "'front'", 'max_length': '5', 'blank': 'True'}),
            'power': ('contrib.fields.NullCharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'rules': ('contrib.fields.NullTextField', [], {'null': 'True'}),
            'sub_number': ('contrib.fields.NullCharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'thoughtness': ('contrib.fields.NullCharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'type_line': ('contrib.fields.NullCharField', [], {'max_length': '255'}),
            'types': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['oracle.CardType']", 'symmetrical': 'False'})
        },
        u'oracle.cardimage': {
            'Meta': {'object_name': 'CardImage'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oracle.Artist']", 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mvid': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'scan': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'oracle.cardimagethumb': {
            'Meta': {'unique_together': "(('original', 'format'),)", 'object_name': 'CardImageThumb'},
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oracle.CardImage']"})
        },
        u'oracle.cardl10n': {
            'Meta': {'unique_together': "(('card_face', 'card_release', 'language'),)", 'object_name': 'CardL10n'},
            'art': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oracle.CardImage']", 'null': 'True', 'blank': 'True'}),
            'card_face': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oracle.CardFace']", 'blank': 'True'}),
            'card_release': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oracle.CardRelease']", 'blank': 'True'}),
            'flavor': ('contrib.fields.NullTextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('contrib.fields.NullCharField', [], {'default': "'en'", 'max_length': '2', 'blank': 'True'}),
            'name': ('contrib.fields.NullCharField', [], {'max_length': '255'}),
            'rules': ('contrib.fields.NullTextField', [], {'null': 'True', 'blank': 'True'}),
            'type_line': ('contrib.fields.NullCharField', [], {'max_length': '255'})
        },
        u'oracle.cardrelease': {
            'Meta': {'object_name': 'CardRelease'},
            'art': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oracle.CardImage']", 'null': 'True', 'blank': 'True'}),
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oracle.Card']"}),
            'card_number': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'card_set': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oracle.CardSet']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rarity': ('contrib.fields.NullCharField', [], {'max_length': '1'})
        },
        u'oracle.cardset': {
            'Meta': {'object_name': 'CardSet'},
            'acronym': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'cards': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'released_at': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'oracle.cardtype': {
            'Meta': {'object_name': 'CardType'},
            'category': ('contrib.fields.NullCharField', [], {'max_length': '9'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('contrib.fields.NullCharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['oracle']
