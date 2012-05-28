from django.contrib.auth.models import User
from django.db import transaction
from wjzpw.web import models

@transaction.commit_on_success
def create_user(**kwargs):
    """
    Creates and saves a User with the given field values.
    """
    user = User.objects.create_user(kwargs['username'], kwargs['email'], kwargs['password'])

    del kwargs['username']
    del kwargs['email']
    del kwargs['password']

    user_profile = models.UserProfile.objects.create(user=user, type=0, **kwargs)

    return user_profile

@transaction.commit_on_success
def create_company(**kwargs):
    """
    Creates and saves a company with the given field values.
    """
    user = User.objects.create_user(kwargs['username'], kwargs['email'], kwargs['password'])

    del kwargs['username']
    del kwargs['email']
    del kwargs['password']


    user_profile = models.UserProfile.objects.create(user=user, type=1, **kwargs)

    return user_profile