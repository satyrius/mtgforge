# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'CardL10n'
        db.create_table('oracle_cardl10n', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('card_face', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oracle.CardFace'])),
            ('card_release', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oracle.CardRelease'])),
            ('language', self.gf('contrib.fields.NullCharField')(max_length=2)),
            ('name', self.gf('contrib.fields.NullCharField')(max_length=255)),
            ('type_line', self.gf('contrib.fields.NullCharField')(max_length=255)),
            ('rules', self.gf('contrib.fields.NullTextField')()),
            ('flavor', self.gf('contrib.fields.NullTextField')(blank=True)),
        ))
        db.send_create_signal('oracle', ['CardL10n'])

        # Adding model 'CardFace'
        db.create_table('oracle_cardface', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oracle.Card'])),
            ('place', self.gf('contrib.fields.NullCharField')(max_length=5)),
            ('mana_cost', self.gf('contrib.fields.NullCharField')(max_length=20, blank=True)),
            ('cmc', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('name', self.gf('contrib.fields.NullCharField')(max_length=255)),
            ('type_line', self.gf('contrib.fields.NullCharField')(max_length=255)),
            ('rules', self.gf('contrib.fields.NullTextField')(max_length=255)),
            ('flavor', self.gf('contrib.fields.NullTextField')(blank=True)),
            ('power', self.gf('contrib.fields.NullCharField')(max_length=10, null=True, blank=True)),
            ('thoughtness', self.gf('contrib.fields.NullCharField')(max_length=10, null=True)),
            ('fixed_power', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('fixed_thoughtness', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('loyality', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('oracle', ['CardFace'])

        # Adding M2M table for field types on 'CardFace'
        db.create_table('oracle_cardface_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cardface', models.ForeignKey(orm['oracle.cardface'], null=False)),
            ('cardtype', models.ForeignKey(orm['oracle.cardtype'], null=False))
        ))
        db.create_unique('oracle_cardface_types', ['cardface_id', 'cardtype_id'])

        # Adding model 'Artist'
        db.create_table('oracle_artist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('contrib.fields.NullCharField')(max_length=255)),
        ))
        db.send_create_signal('oracle', ['Artist'])

        # Adding model 'CardType'
        db.create_table('oracle_cardtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('contrib.fields.NullCharField')(unique=True, max_length=255)),
            ('category', self.gf('contrib.fields.NullCharField')(max_length=9)),
        ))
        db.send_create_signal('oracle', ['CardType'])

        # Adding model 'CardRelease'
        db.create_table('oracle_cardrelease', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oracle.Card'])),
            ('card_set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oracle.CardSet'])),
            ('rarity', self.gf('contrib.fields.NullCharField')(max_length=1)),
            ('card_number', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('artist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oracle.Artist'])),
        ))
        db.send_create_signal('oracle', ['CardRelease'])

        # Adding model 'Card'
        db.create_table('oracle_card', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('oracle', ['Card'])


    def backwards(self, orm):
        
        # Deleting model 'CardL10n'
        db.delete_table('oracle_cardl10n')

        # Deleting model 'CardFace'
        db.delete_table('oracle_cardface')

        # Removing M2M table for field types on 'CardFace'
        db.delete_table('oracle_cardface_types')

        # Deleting model 'Artist'
        db.delete_table('oracle_artist')

        # Deleting model 'CardType'
        db.delete_table('oracle_cardtype')

        # Deleting model 'CardRelease'
        db.delete_table('oracle_cardrelease')

        # Deleting model 'Card'
        db.delete_table('oracle_card')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'place': ('contrib.fields.NullCharField', [], {'max_length': '5'}),
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
