# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding field 'CardSet.name_en'
        db.add_column('oracle_cardset', 'name_en', self.gf('contrib.fields.NullCharField')(max_length=255, unique=True, null=True, blank=True), keep_default=False)

        # Adding field 'CardSet.name_ru'
        db.add_column('oracle_cardset', 'name_ru', self.gf('contrib.fields.NullCharField')(max_length=255, unique=True, null=True, blank=True), keep_default=False)


    def backwards(self, orm):

        # Deleting field 'CardSet.name_ru'
        db.delete_column('oracle_cardset', 'name_ru')

        # Deleting field 'CardSet.name_en'
        db.delete_column('oracle_cardset', 'name_en')


    models = {
        'oracle.cardset': {
            'Meta': {'object_name': 'CardSet'},
            'acronym': ('contrib.fields.NullCharField', [], {'unique': 'True', 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('contrib.fields.NullCharField', [], {'unique': 'True', 'max_length': '255'}),
            'name_en': ('contrib.fields.NullCharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('contrib.fields.NullCharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['oracle']
