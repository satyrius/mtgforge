# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DataProvider'
        db.create_table('oracle_dataprovider', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('home', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('oracle', ['DataProvider'])

        # Adding model 'DataSource'
        db.create_table('oracle_datasource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('data_provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oracle.DataProvider'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('oracle', ['DataSource'])

        # Adding unique constraint on 'DataSource', fields ['content_type', 'object_id', 'url']
        db.create_unique('oracle_datasource', ['content_type_id', 'object_id', 'url'])

        # Adding unique constraint on 'DataSource', fields ['content_type', 'object_id', 'data_provider']
        db.create_unique('oracle_datasource', ['content_type_id', 'object_id', 'data_provider_id'])

        # Adding model 'DataProviderPage'
        db.create_table('oracle_dataproviderpage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('url_hash', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('data_provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oracle.DataProvider'], null=True, blank=True)),
            ('content', self.gf('contrib.fields.NullTextField')()),
            ('class_name', self.gf('contrib.fields.NullCharField')(max_length=255)),
            ('name', self.gf('contrib.fields.NullCharField')(max_length=255, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal('oracle', ['DataProviderPage'])

        # Adding unique constraint on 'DataProviderPage', fields ['url_hash', 'class_name']
        db.create_unique('oracle_dataproviderpage', ['url_hash', 'class_name'])

        # Adding model 'Card'
        db.create_table('oracle_card', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('contrib.fields.NullCharField')(max_length=255)),
            ('faces_count', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
        ))
        db.send_create_signal('oracle', ['Card'])

        # Adding model 'CardType'
        db.create_table('oracle_cardtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('contrib.fields.NullCharField')(unique=True, max_length=255)),
            ('category', self.gf('contrib.fields.NullCharField')(max_length=9)),
        ))
        db.send_create_signal('oracle', ['CardType'])

        # Adding model 'CardFace'
        db.create_table('oracle_cardface', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oracle.Card'], blank=True)),
            ('place', self.gf('contrib.fields.NullCharField')(default='front', max_length=5, blank=True)),
            ('sub_number', self.gf('contrib.fields.NullCharField')(max_length=1, null=True, blank=True)),
            ('mana_cost', self.gf('contrib.fields.NullCharField')(max_length=255, null=True)),
            ('cmc', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('color_identity', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0, blank=True)),
            ('colors', self.gf('arrayfields.fields.IntegerArrayField')(default=[], blank=True)),
            ('name', self.gf('contrib.fields.NullCharField')(unique=True, max_length=255)),
            ('type_line', self.gf('contrib.fields.NullCharField')(max_length=255)),
            ('rules', self.gf('contrib.fields.NullTextField')(null=True)),
            ('power', self.gf('contrib.fields.NullCharField')(max_length=10, null=True, blank=True)),
            ('thoughtness', self.gf('contrib.fields.NullCharField')(max_length=10, null=True, blank=True)),
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

        # Adding model 'CardSet'
        db.create_table('oracle_cardset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True, null=True, blank=True)),
            ('name_ru', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True, null=True, blank=True)),
            ('name_tw', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True, null=True, blank=True)),
            ('name_cn', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True, null=True, blank=True)),
            ('name_de', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True, null=True, blank=True)),
            ('name_fr', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True, null=True, blank=True)),
            ('name_it', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True, null=True, blank=True)),
            ('name_jp', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True, null=True, blank=True)),
            ('name_ko', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True, null=True, blank=True)),
            ('name_pt', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True, null=True, blank=True)),
            ('name_es', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True, null=True, blank=True)),
            ('acronym', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
            ('cards', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('released_at', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('oracle', ['CardSet'])

        # Adding model 'Artist'
        db.create_table('oracle_artist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('contrib.fields.NullCharField')(max_length=255)),
        ))
        db.send_create_signal('oracle', ['Artist'])

        # Adding model 'CardImage'
        db.create_table('oracle_cardimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mvid', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, null=True, blank=True)),
            ('scan', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('file', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('artist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oracle.Artist'], null=True, blank=True)),
        ))
        db.send_create_signal('oracle', ['CardImage'])

        # Adding model 'CardImageThumb'
        db.create_table('oracle_cardimagethumb', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oracle.CardImage'])),
            ('format', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('file', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('oracle', ['CardImageThumb'])

        # Adding unique constraint on 'CardImageThumb', fields ['original', 'format']
        db.create_unique('oracle_cardimagethumb', ['original_id', 'format'])

        # Adding model 'CardRelease'
        db.create_table('oracle_cardrelease', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oracle.Card'])),
            ('card_set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oracle.CardSet'])),
            ('rarity', self.gf('contrib.fields.NullCharField')(max_length=1)),
            ('card_number', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('art', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oracle.CardImage'], null=True, blank=True)),
        ))
        db.send_create_signal('oracle', ['CardRelease'])

        # Adding model 'CardL10n'
        db.create_table('oracle_cardl10n', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('card_face', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oracle.CardFace'], blank=True)),
            ('card_release', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oracle.CardRelease'], blank=True)),
            ('language', self.gf('contrib.fields.NullCharField')(default='en', max_length=2, blank=True)),
            ('name', self.gf('contrib.fields.NullCharField')(max_length=255)),
            ('type_line', self.gf('contrib.fields.NullCharField')(max_length=255)),
            ('rules', self.gf('contrib.fields.NullTextField')(null=True, blank=True)),
            ('flavor', self.gf('contrib.fields.NullTextField')(null=True, blank=True)),
            ('art', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oracle.CardImage'], null=True, blank=True)),
        ))
        db.send_create_signal('oracle', ['CardL10n'])

        # Adding unique constraint on 'CardL10n', fields ['card_face', 'card_release', 'language']
        db.create_unique('oracle_cardl10n', ['card_face_id', 'card_release_id', 'language'])


    def backwards(self, orm):
        # Removing unique constraint on 'CardL10n', fields ['card_face', 'card_release', 'language']
        db.delete_unique('oracle_cardl10n', ['card_face_id', 'card_release_id', 'language'])

        # Removing unique constraint on 'CardImageThumb', fields ['original', 'format']
        db.delete_unique('oracle_cardimagethumb', ['original_id', 'format'])

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

        # Deleting model 'Card'
        db.delete_table('oracle_card')

        # Deleting model 'CardType'
        db.delete_table('oracle_cardtype')

        # Deleting model 'CardFace'
        db.delete_table('oracle_cardface')

        # Removing M2M table for field types on 'CardFace'
        db.delete_table('oracle_cardface_types')

        # Deleting model 'CardSet'
        db.delete_table('oracle_cardset')

        # Deleting model 'Artist'
        db.delete_table('oracle_artist')

        # Deleting model 'CardImage'
        db.delete_table('oracle_cardimage')

        # Deleting model 'CardImageThumb'
        db.delete_table('oracle_cardimagethumb')

        # Deleting model 'CardRelease'
        db.delete_table('oracle_cardrelease')

        # Deleting model 'CardL10n'
        db.delete_table('oracle_cardl10n')


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
            'sub_number': ('contrib.fields.NullCharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'thoughtness': ('contrib.fields.NullCharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'type_line': ('contrib.fields.NullCharField', [], {'max_length': '255'}),
            'types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['oracle.CardType']", 'symmetrical': 'False'})
        },
        'oracle.cardimage': {
            'Meta': {'object_name': 'CardImage'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oracle.Artist']", 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mvid': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'scan': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'oracle.cardimagethumb': {
            'Meta': {'unique_together': "(('original', 'format'),)", 'object_name': 'CardImageThumb'},
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oracle.CardImage']"})
        },
        'oracle.cardl10n': {
            'Meta': {'unique_together': "(('card_face', 'card_release', 'language'),)", 'object_name': 'CardL10n'},
            'art': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oracle.CardImage']", 'null': 'True', 'blank': 'True'}),
            'card_face': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oracle.CardFace']", 'blank': 'True'}),
            'card_release': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oracle.CardRelease']", 'blank': 'True'}),
            'flavor': ('contrib.fields.NullTextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('contrib.fields.NullCharField', [], {'default': "'en'", 'max_length': '2', 'blank': 'True'}),
            'name': ('contrib.fields.NullCharField', [], {'max_length': '255'}),
            'rules': ('contrib.fields.NullTextField', [], {'null': 'True', 'blank': 'True'}),
            'type_line': ('contrib.fields.NullCharField', [], {'max_length': '255'})
        },
        'oracle.cardrelease': {
            'Meta': {'object_name': 'CardRelease'},
            'art': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oracle.CardImage']", 'null': 'True', 'blank': 'True'}),
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oracle.Card']"}),
            'card_number': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'card_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oracle.CardSet']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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