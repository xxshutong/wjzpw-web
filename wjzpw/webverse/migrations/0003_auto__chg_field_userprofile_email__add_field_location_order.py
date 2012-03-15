# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'UserProfile.email'
        db.alter_column('webverse_userprofile', 'email', self.gf('django.db.models.fields.EmailField')(max_length=80))

        # Adding field 'Location.order'
        db.add_column('webverse_location', 'order', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2), keep_default=False)


    def backwards(self, orm):
        
        # Changing field 'UserProfile.email'
        db.alter_column('webverse_userprofile', 'email', self.gf('django.db.models.fields.EmailField')(max_length=75))

        # Deleting field 'Location.order'
        db.delete_column('webverse_location', 'order')


    models = {
        'webverse.abstractmodel': {
            'Meta': {'object_name': 'AbstractModel'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'})
        },
        'webverse.announcement': {
            'Meta': {'object_name': 'Announcement', '_ormbases': ['webverse.AbstractModel']},
            'abstractmodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['webverse.AbstractModel']", 'unique': 'True', 'primary_key': 'True'}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
            'end_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'webverse.city': {
            'Meta': {'object_name': 'City'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webverse.Province']"}),
            'spell': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'})
        },
        'webverse.configuration': {
            'Meta': {'object_name': 'Configuration'},
            'hot_line_one': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'hot_line_two': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'qq': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'webverse.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'})
        },
        'webverse.friendlylink': {
            'Meta': {'object_name': 'FriendlyLink'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'web_site': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'webverse.industry': {
            'Meta': {'object_name': 'Industry'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'spell': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        'webverse.job': {
            'Meta': {'object_name': 'Job', '_ormbases': ['webverse.AbstractModel']},
            'abstractmodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['webverse.AbstractModel']", 'unique': 'True', 'primary_key': 'True'}),
            'age': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webverse.UserProfile']"}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'edu_background': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webverse.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'salary': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'sex': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'work_experience': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'})
        },
        'webverse.location': {
            'Meta': {'object_name': 'Location'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'spell': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'webverse.province': {
            'Meta': {'object_name': 'Province'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'spell': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'})
        },
        'webverse.service': {
            'Meta': {'object_name': 'Service'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'period': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'price': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'webverse.userprofile': {
            'Meta': {'object_name': 'UserProfile', '_ormbases': ['webverse.AbstractModel']},
            'abstractmodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['webverse.AbstractModel']", 'unique': 'True', 'primary_key': 'True'}),
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'census': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webverse.City']"}),
            'cp_accept_notice': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'cp_address': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'}),
            'cp_contact': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'cp_fax': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'cp_industry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webverse.Industry']"}),
            'cp_intro': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'cp_license': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'cp_mobile_phone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'cp_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'cp_postcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'cp_scope': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'cp_service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webverse.Service']", 'null': 'True', 'blank': 'True'}),
            'cp_service_begin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cp_telephone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'cp_website': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '80'}),
            'expires': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.IntegerField', [], {'default': '2', 'max_length': '2'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'job_state': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'job_type': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webverse.Location']"}),
            'mobile_phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'points_balance': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'qq': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'real_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'stature': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'wedding': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'work_years': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['webverse']
