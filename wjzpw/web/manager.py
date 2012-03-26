#from django.db import models
#import datetime
#from django.contrib.auth.models import get_hexdigest
#
#UNUSABLE_PASSWORD = '!' # This will never be a valid hash
#
#class UserProfileManager(models.Manager):
#    def create_user(self, **kwargs):
#        """
#        Creates and saves a User with the given field values.
#        """
#        now = datetime.datetime.now()
#
#        user_profile = self.model(last_login=now, date_joined=now, **kwargs)
#        user_profile.email = user_profile.email.lower()
#        user_profile.password = self.wrap_password(user_profile.password)
#        return user_profile
#
#    @classmethod
#    def wrap_password(cls, raw_password):
#        if raw_password is None:
#            return UNUSABLE_PASSWORD
#        else:
#            import random
#            algo = 'sha1'
#            salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
#            hsh = get_hexdigest(algo, salt, raw_password)
#            return '%s$%s$%s' % (algo, salt, hsh)
#
#    def check_password(self, raw_password):
#        """
#        Returns a boolean of whether the raw_password was correct. Handles
#        encryption formats behind the scenes.
#        """
#        # Backwards-compatibility check. Older passwords won't include the
#        # algorithm or salt.
#        if '$' not in self.password:
#            is_correct = (self.password == get_hexdigest('md5', '', raw_password))
#            if is_correct:
#                # Convert the password to the new, more secure format.
#                self.set_password(raw_password)
#                self.save()
#            return is_correct
#        return check_password(raw_password, self.password)