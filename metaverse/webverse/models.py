
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models.fields.related import OneToOneField

# Defines the model for Digido.
#
# NOTE!!
#  # DO NOT NAME attribute with "id" or "*_id". The publishing code will weed
#    those out as keys and not include them in the serialization.
#
#  * Use south migration tool to generate the migration script.
#        manage.py schemamigration webverse --auto
#        manage.py migrate

class UserProfile(models.Model):
    """
    Profile for any users with access to the system.
    Points are updated here but can be computed by the awarded points - redeemed points. For performance.
    """
    USER_TYPE = (
        (0, 'Parent'),
        (1, 'Child')
    )

    GENDER = (
        (0, 'male'),
        (1, 'female'),
        (2, 'not-specified')
    )

    user = OneToOneField(User)
    username = models.CharField('Username', max_length=50, null=True, blank=False)
    realname = models.CharField('Real Name', max_length=50, null=True, blank=False)
    type = models.IntegerField('User Type', max_length=2, choices=USER_TYPE, default=0)
    email = models.EmailField('Email', )
    gender = models.IntegerField('Gender', max_length=2, choices=GENDER, default=2)
    birthdate = models.DateField('Birthdate', null=True, blank=True)
    points_balance = models.IntegerField('Points', default=0)
    parent_id = models.IntegerField("Parent id", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    #facebook information
    access_token = models.CharField(max_length=1024, unique=True, null=True, blank=True)
    expires = models.IntegerField(null=True, blank=True)
    uid = models.BigIntegerField(unique=True, null=True, blank=True)
    is_deleted = models.BooleanField("Is Deleted", default=False)

    def __unicode__(self):
        return str(self.user.id) + "-" + self.email


class Activity(models.Model):
    """
    Types of action set up to be performed by children.
    """
    name = models.CharField('Activity Name', max_length=256, blank=False)
    points_per_minute = models.IntegerField('Points per minute', default=0)
    image_path = models.ImageField(upload_to='static/upload/images',max_length=255)

    def __unicode__(self):
        return self.name


class Participation(models.Model):
    """
    A single act of doing an activity by a child.
    """
    user = models.ForeignKey(UserProfile, name='Participant')
    activity = models.ForeignKey(Activity, name='Activity')
    validated = models.NullBooleanField('Validated')
    duration_minute = models.IntegerField('Duration in Minutes')
    activity_date = models.DateField('Participation Date')
    points_awarded = models.IntegerField('Points Awarded', null=False, blank=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def get_date_duration(self):
        temp = (datetime.date.today() - self.activity_date).days
        return temp

    def __unicode__(self):
        return str(self.user.id) + '-' + self.user.email + '-' + self.activity.name


class Suggestion_Reward(models.Model):
    """
    Reward suggestion for Parents when they are setting the account.
    """
    name = models.CharField('Reward Name', max_length=256, blank=False)
    points_required = models.IntegerField('Points Required', null=False, blank=False, default=0)

    def __unicode__(self):
        return self.name


class Reward(models.Model):
    """
    Incentives setup by Parent for child to earn points and redeem.
    Eligibility allows parent to pick which child can redeem this reward.
    """
    user = models.ForeignKey(UserProfile, related_name='owner')
    name = models.CharField('Reward Name', max_length=256, blank=False)
    points_required = models.IntegerField('Points Required', null=False, blank=False, default=0)
    eligibility = models.ManyToManyField(UserProfile, through='UserReward')
    is_deleted = models.BooleanField("Is Deleted", default=False)

    def __unicode__(self):
        return self.name


class Redemption(models.Model):
    """
    Who redeem which reward. Points deducted are recorded in case the points required for reward changed.
    """
    user = models.ForeignKey(UserProfile, name='Who redeem it?')
    reward = models.ForeignKey(Reward)
    validated = models.NullBooleanField('Validated')
    validated_date = models.DateField('Validate Date', null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return str(self.user.id) + '-' + self.user.email + '-' + self.reward.name


class Badge(models.Model):
    """
    Achievement setup by admin to award participation.
    """
    name = models.CharField('Badge Name', max_length=256, blank=False)
    description = models.CharField('Badge Description', max_length=1024, blank=False)
    activity = models.ForeignKey(Activity, name='Activity Participated', null=True, blank=True)
    duration_minute = models.IntegerField('Duration in Minutes', null=True, blank=True, default=0)
    participation_count = models.IntegerField('Number of participation', null=True, blank=True, default=0)
    consecutive_count = models.IntegerField('Number of consecutive day participation', null=True, blank=True, default=0)
    day_range = models.IntegerField('Range of days where above criteria has to be met', null=True, blank=True, default=0)
    image_path = models.ImageField(upload_to='static/upload/images',max_length=255)

    def __unicode__(self):
        return self.name


class Achievement(models.Model):
    """
    Badges earned by user.
    """
    user = models.ForeignKey(UserProfile)
    badge = models.ForeignKey(Badge)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return str(self.user.id) + '-' + self.user.email + '-' + self.badge.name


class UserReward(models.Model):
    """
    Store the relationship between kids and rewards, when parent create a new reward
    """
    user = models.ForeignKey(UserProfile)
    reward = models.ForeignKey(Reward)

    def __unicode__(self):
        return str(self.user.id) + '-' + self.user.email + '-' + self.reward.name

