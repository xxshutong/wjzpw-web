# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Participation'
        db.create_table('webverse_participation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webverse.Activity'])),
            ('validated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('duration_minute', self.gf('django.db.models.fields.IntegerField')()),
            ('activity_date', self.gf('django.db.models.fields.DateField')()),
            ('points_awarded', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal('webverse', ['Participation'])

        # Adding model 'Badge'
        db.create_table('webverse_badge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webverse.Activity'])),
            ('duration_minute', self.gf('django.db.models.fields.IntegerField')()),
            ('participation_count', self.gf('django.db.models.fields.IntegerField')()),
            ('consecutive_count', self.gf('django.db.models.fields.IntegerField')()),
            ('day_range', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('webverse', ['Badge'])

        # Adding model 'Achievement'
        db.create_table('webverse_achievement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('badge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webverse.Badge'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal('webverse', ['Achievement'])

        # Adding model 'Redemption'
        db.create_table('webverse_redemption', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('reward', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webverse.Reward'])),
            ('points_deducted', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal('webverse', ['Redemption'])

        # Adding model 'Reward'
        db.create_table('webverse_reward', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='owner', to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('points_required', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('eligibility', self.gf('django.db.models.fields.related.ForeignKey')(related_name='eligible', to=orm['auth.User'])),
        ))
        db.send_create_signal('webverse', ['Reward'])

        # Adding model 'Suggestion_Reward'
        db.create_table('webverse_suggestion_reward', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('points_required', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('webverse', ['Suggestion_Reward'])

        # Changing field 'Activity.points_per_minute'
        db.alter_column('webverse_activity', 'points_per_minute', self.gf('django.db.models.fields.IntegerField')())

        # Adding field 'UserProfile.points_balance'
        db.add_column('webverse_userprofile', 'points_balance', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'UserProfile.created_at'
        db.add_column('webverse_userprofile', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True), keep_default=False)

        # Adding field 'UserProfile.updated_at'
        db.add_column('webverse_userprofile', 'updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'Participation'
        db.delete_table('webverse_participation')

        # Deleting model 'Badge'
        db.delete_table('webverse_badge')

        # Deleting model 'Achievement'
        db.delete_table('webverse_achievement')

        # Deleting model 'Redemption'
        db.delete_table('webverse_redemption')

        # Deleting model 'Reward'
        db.delete_table('webverse_reward')

        # Deleting model 'Suggestion_Reward'
        db.delete_table('webverse_suggestion_reward')

        # Changing field 'Activity.points_per_minute'
        db.alter_column('webverse_activity', 'points_per_minute', self.gf('django.db.models.fields.IntegerField')(max_length=4))

        # Deleting field 'UserProfile.points_balance'
        db.delete_column('webverse_userprofile', 'points_balance')

        # Deleting field 'UserProfile.created_at'
        db.delete_column('webverse_userprofile', 'created_at')

        # Deleting field 'UserProfile.updated_at'
        db.delete_column('webverse_userprofile', 'updated_at')


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
        'webverse.achievement': {
            'Meta': {'object_name': 'Achievement'},
            'badge': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webverse.Badge']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'webverse.activity': {
            'Meta': {'object_name': 'Activity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'points_per_minute': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'webverse.badge': {
            'Meta': {'object_name': 'Badge'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webverse.Activity']"}),
            'consecutive_count': ('django.db.models.fields.IntegerField', [], {}),
            'day_range': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'duration_minute': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'participation_count': ('django.db.models.fields.IntegerField', [], {})
        },
        'webverse.participation': {
            'Meta': {'object_name': 'Participation'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webverse.Activity']"}),
            'activity_date': ('django.db.models.fields.DateField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'duration_minute': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'points_awarded': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'webverse.redemption': {
            'Meta': {'object_name': 'Redemption'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'points_deducted': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'reward': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webverse.Reward']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'webverse.reward': {
            'Meta': {'object_name': 'Reward'},
            'eligibility': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'eligible'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'points_required': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner'", 'to': "orm['auth.User']"})
        },
        'webverse.suggestion_reward': {
            'Meta': {'object_name': 'Suggestion_Reward'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'points_required': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'webverse.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'birthdate': ('django.db.models.fields.DateField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'gender': ('django.db.models.fields.IntegerField', [], {'default': '2', 'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'points_balance': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['webverse']
