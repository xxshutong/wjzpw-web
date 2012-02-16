from django.contrib.auth import models as auth_models
from wjzpw.webverse.models import UserProfile

class FacebookBackend:
    def authenticate(self, email=None, token=None):
        #TODO: Get the email address from access token and see if it matches email provided.
        try:
            profile = UserProfile.objects.get(email=email)
            return profile.user
        except Exception:
            return None

    def get_user(self, user_id):

        try:
            return auth_models.User.objects.get(pk=user_id)
        except auth_models.User.DoesNotExist:
            return None