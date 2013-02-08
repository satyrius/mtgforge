# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.execute('delete from forge_cardftsindex')
        # Changing field 'CardFtsIndex.card_face'
        db.alter_column('forge_cardftsindex', 'card_face_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['oracle.CardFace']))

    def backwards(self, orm):
        # Changing field 'CardFtsIndex.card_face'
        db.alter_column('forge_cardftsindex', 'card_face_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oracle.CardFace'], null=True))

    models = {
        'forge.cardftsindex': {
            'Meta': {'object_name': 'CardFtsIndex'},
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oracle.Card']"}),
            'card_face': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oracle.CardFace']"}),
            'cmc': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'color_identity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'forge.cardsimilarity': {
            'Meta': {'object_name': 'CardSimilarity'},
            'alias': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forge.CardSimilarity']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
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
            'flavor': ('contrib.fields.NullTextField', [], {'null': 'True'}),
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
        'oracle.cardtype': {
            'Meta': {'object_name': 'CardType'},
            'category': ('contrib.fields.NullCharField', [], {'max_length': '9'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('contrib.fields.NullCharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['forge']
