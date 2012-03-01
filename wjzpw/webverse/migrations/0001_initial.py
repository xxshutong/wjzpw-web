# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'AbstractModel'
        db.create_table('webverse_abstractmodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal('webverse', ['AbstractModel'])

        # Adding model 'Province'
        db.create_table('webverse_province', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('spell', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('webverse', ['Province'])

        # Adding model 'City'
        db.create_table('webverse_city', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('spell', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('province', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webverse.Province'])),
        ))
        db.send_create_signal('webverse', ['City'])

        # Adding model 'Location'
        db.create_table('webverse_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('spell', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('webverse', ['Location'])

        # Adding model 'Industry'
        db.create_table('webverse_industry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('spell', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('webverse', ['Industry'])

        # Adding model 'Service'
        db.create_table('webverse_service', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('period', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
            ('price', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('webverse', ['Service'])

        # Adding model 'UserProfile'
        db.create_table('webverse_userprofile', (
            ('abstractmodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['webverse.AbstractModel'], unique=True, primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('realname', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('gender', self.gf('django.db.models.fields.IntegerField')(default=2, max_length=2)),
            ('birthday', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('census', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webverse.City'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webverse.Location'])),
            ('mobile_phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('qq', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('wedding', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
            ('stature', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('weight', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('job_state', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
            ('job_type', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
            ('work_years', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('points_balance', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('cp_accept_notice', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('cp_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('cp_license', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('cp_industry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webverse.Industry'])),
            ('cp_scope', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
            ('cp_intro', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('cp_address', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True)),
            ('cp_postcode', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('cp_contact', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('cp_telephone', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('cp_mobile_phone', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('cp_fax', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('cp_website', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('cp_service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webverse.Service'], null=True, blank=True)),
            ('cp_service_begin', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('access_token', self.gf('django.db.models.fields.CharField')(max_length=1024, unique=True, null=True, blank=True)),
            ('expires', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('webverse', ['UserProfile'])

        # Adding model 'Job'
        db.create_table('webverse_job', (
            ('abstractmodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['webverse.AbstractModel'], unique=True, primary_key=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webverse.UserProfile'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('salary', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('number', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webverse.Location'])),
            ('edu_background', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
            ('work_experience', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
            ('age', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
            ('sex', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=2000)),
        ))
        db.send_create_signal('webverse', ['Job'])

        # Adding model 'Feedback'
        db.create_table('webverse_feedback', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=2000)),
        ))
        db.send_create_signal('webverse', ['Feedback'])

        # Adding model 'Announcement'
        db.create_table('webverse_announcement', (
            ('abstractmodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['webverse.AbstractModel'], unique=True, primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=10000)),
            ('end_date', self.gf('django.db.models.fields.DateField')(blank=True)),
        ))
        db.send_create_signal('webverse', ['Announcement'])

        # Adding model 'FriendlyLink'
        db.create_table('webverse_friendlylink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('web_site', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('webverse', ['FriendlyLink'])

        # Adding model 'Configuration'
        db.create_table('webverse_configuration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hot_line_one', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('hot_line_two', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('qq', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('webverse', ['Configuration'])


    def backwards(self, orm):
        
        # Deleting model 'AbstractModel'
        db.delete_table('webverse_abstractmodel')

        # Deleting model 'Province'
        db.delete_table('webverse_province')

        # Deleting model 'City'
        db.delete_table('webverse_city')

        # Deleting model 'Location'
        db.delete_table('webverse_location')

        # Deleting model 'Industry'
        db.delete_table('webverse_industry')

        # Deleting model 'Service'
        db.delete_table('webverse_service')

        # Deleting model 'UserProfile'
        db.delete_table('webverse_userprofile')

        # Deleting model 'Job'
        db.delete_table('webverse_job')

        # Deleting model 'Feedback'
        db.delete_table('webverse_feedback')

        # Deleting model 'Announcement'
        db.delete_table('webverse_announcement')

        # Deleting model 'FriendlyLink'
        db.delete_table('webverse_friendlylink')

        # Deleting model 'Configuration'
        db.delete_table('webverse_configuration')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
            'expires': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.IntegerField', [], {'default': '2', 'max_length': '2'}),
            'job_state': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'job_type': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webverse.Location']"}),
            'mobile_phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'points_balance': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'qq': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'realname': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'stature': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'wedding': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'work_years': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['webverse']
