from django.contrib.auth.models import User
from wjzpw.webverse.models import UserProfile
from wjzpw.webverse.utils import generate_base64_string

class UserManager(object):
    @staticmethod
    def get_childs_by_parent_id(parent_id):
        try:
            return UserProfile.objects.filter(parent_id=parent_id, is_deleted = False).all().order_by('username')
        except UserProfile.DoesNotExist:
            return None
        except Exception:
            return None

    @staticmethod
    def get_auth_user(username_or_mail, password):
        """Get user by username/email and password
        """
        if '@' in username_or_mail:
            kwargs = {'email': username_or_mail}
        else:
            kwargs = {'username': username_or_mail}
        try:
            user = User.objects.get(**kwargs)
            return user
        except User.DoesNotExist:
            return None
        
    @staticmethod
    def get_user_profile(user_id):
        try:
            return UserProfile.objects.get(user=user_id, is_deleted = False)
        except User.DoesNotExist:
            return None
        except Exception:
            return None

    @staticmethod
    def get_user_profile_by_id(user_profile_id):
        try:
            return UserProfile.objects.get(id=user_profile_id, is_deleted = False)
        except User.DoesNotExist:
            return None
        except Exception:
            return None

    @staticmethod
    def get_children_by_parent(parent):
        """Return  children list by parent.
    """
        try:
            users = UserProfile.objects.filter(parent_id=parent.id, is_deleted = False)
            return users
        except Exception:
            return None

    @staticmethod
    def delete_kid_profile(user_id):
        try:
            users = UserProfile.objects.filter(id=user_id)
            if users:
                user_name = str(users[0].user.username) + '_deleted'
                user_name = generate_base64_string(user_name)
                kid = User.objects.filter(id = users[0].user.id)
                kid.update(username = user_name)
                users.update(is_deleted = True)
                return True
        except Exception:
            return False


        
