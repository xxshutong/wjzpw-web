from django.db import models
import datetime

class UserProfileManager(models.Manager):
    def create_user(self, **kwargs):
        """
        Creates and saves a User with the given field values.
        """
        now = datetime.datetime.now()

        # Normalize the address by lowercasing the domain part of the email
        # address.
        try:
            email_name, domain_part = kwargs['email'].strip().split('@', 1)
        except ValueError:
            pass
        else:
            kwargs['email'] = '@'.join([email_name, domain_part.lower()])

        user_profile = self.model(last_login=now, date_joined=now, **kwargs)

        user_profile.set_password(user_profile.password)
        user_profile.save(using=self._db)
        return user_profile