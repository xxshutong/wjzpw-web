# coding: utf-8

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
    if kwargs.get("is_edit", False):
        # 更新
        user = User.objects.get(username=kwargs.get("username"))
        user.email = kwargs['email']
        user.save()
    else:
        # 注册
        user = User.objects.create_user(kwargs['username'], kwargs['email'], kwargs['password'])

    del kwargs['username']
    del kwargs['email']
    del kwargs['password']

    if kwargs.get("is_edit", False):
        # 更新
        user_profile = models.UserProfile.objects.get(user=user)
        del kwargs['is_edit']
        user_profile.__dict__.update(**kwargs)
        user_profile.cp_service = kwargs['cp_service']
        user_profile.cp_service_id = kwargs['cp_service'].id
        user_profile.cp_industry = kwargs['cp_industry']
        user_profile.cp_industry_id = kwargs['cp_industry'].id
        user_profile.location = kwargs['location']
        user_profile.location_id = kwargs['location'].id
        user_profile.save()
    else:
        # 注册
        del kwargs['is_edit']
        user_profile = models.UserProfile.objects.create(user=user, type=1, **kwargs)

    return user_profile