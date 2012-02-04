# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Card.name'
        db.add_column('oracle_card', 'name', self.gf('contrib.fields.NullCharField')(default='', max_length=255, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Card.name'
        db.delete_column('oracle_card', 'name')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('contrib.fields.NullCharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'oracle.cardface': {
            'Meta': {'object_name': 'CardFace'},
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oracle.Card']"}),
            'cmc': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fixed_power': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fixed_thoughtness': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'flavor': ('contrib.fields.NullTextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loyality': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mana_cost': ('contrib.fields.NullCharField', [], {'max_length': '20', 'blank': 'True'}),
            'name': ('contrib.fields.NullCharField', [], {'max_length': '255'}),
            'place': ('contrib.fields.NullCharField', [], {'default': "'front'", 'max_length': '5'}),
            'power': ('contrib.fields.NullCharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'rules': ('contrib.fields.NullTextField', [], {'max_length': '255'}),
            'thoughtness': ('contrib.fields.NullCharField', [], {'max_length': '10', 'null': 'True'}),
            'type_line': ('contrib.fields.NullCharField', [], {'max_length': '255'}),
            'types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['oracle.CardType']", 'symmetrical': 'False'})
        },
        'oracle.cardl10n': {
            'Meta': {'object_name': 'CardL10n'},
            'card_face': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oracle.CardFace']"}),
            'card_release': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oracle.CardRelease']"}),
            'flavor': ('contrib.fields.NullTextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('contrib.fields.NullCharField', [], {'max_length': '2'}),
            'name': ('contrib.fields.NullCharField', [], {'max_length': '255'}),
            'rules': ('contrib.fields.NullTextField', [], {}),
            'type_line': ('contrib.fields.NullCharField', [], {'max_length': '255'})
        },
        'oracle.cardrelease': {
            'Meta': {'object_name': 'CardRelease'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oracle.Artist']"}),
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oracle.Card']"}),
            'card_number': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'card_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oracle.CardSet']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rarity': ('contrib.fields.NullCharField', [], {'max_length': '1'})
        },
        'oracle.cardset': {
            'Meta': {'object_name': 'CardSet'},
            'acronym': ('contrib.fields.NullCharField', [], {'unique': 'True', 'max_length': '10'}),
            'cards': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('contrib.fields.NullCharField', [], {'unique': 'True', 'max_length': '255'}),
            'name_en': ('contrib.fields.NullCharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('contrib.fields.NullCharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
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
