import datetime
import logging
from wjzpw.webverse.model.users import UserManager
from wjzpw.webverse.models import Suggestion_Reward, UserReward
from wjzpw.webverse.models import Reward, UserProfile, Redemption
from django.db import connection, transaction

class SuggestionRewardManager(object):
    @staticmethod
    def get_all_suggestion_rewards():
        try:
            return Suggestion_Reward.objects.all().order_by('name')
        except Suggestion_Reward.DoesNotExist:
            return None
        except Exception:
            return None

class RewardsManager(object):

    @staticmethod
    def get_rewards_by_child_id(child_id, points):
        cursor = connection.cursor()
        cursor.execute("SELECT rd.name as name, rd.points_required as point_required, rd.id as id, rd.points_required-%s as disparity FROM webverse_reward rd,\
                        webverse_userreward ur where ur.user_id = %s and rd.id = ur.reward_id and rd.is_deleted = False ", [points,child_id])
        rewards = cursor.fetchall()
        result = []
        if rewards:
            for reward in rewards:
                dict = {
                    'name': str(reward[0]),
                    'points_required': int(reward[1]),
                    'id' :int(reward[2]),
                    'disparity' : int(reward[3])
                }
                result.append(dict)
        return result

    @staticmethod
    def get_reward_by_id(reward_id):
        reward = Reward.objects.get(pk=reward_id)
        return reward
    
    @staticmethod
    def get_reward_by_parent_id(parent_id):
        args = {"user" :parent_id, 'is_deleted' :False}
        try:
            return Reward.objects.filter(**args).order_by('name')
        except Reward.DoesNotExist:
            return None
        except Exception:
            return None

    @staticmethod
    @transaction.commit_on_success
    def save_reward(parent_id, reward_name, reward_point, reward_childs):
        try:
            parent = UserManager.get_user_profile_by_id(parent_id)
            reward = Reward()
            reward.name = reward_name
            reward.points_required = reward_point
            reward.user = parent
            reward.save()

            child_ids = reward_childs.split(';')
            if len(child_ids) > 0 and child_ids[0] != '':
                for child_id in child_ids:
                    user_reward = UserReward()
                    user_reward.reward = reward
                    user_reward.user_id = long(child_id)
                    user_reward.save()

            return reward.id
        except Exception, e:
            logging.error("Create participation for kid error, error is %s" % e)
            return None


    @staticmethod
    @transaction.commit_on_success
    def edit_reward(reward, reward_name, reward_point, reward_childs):
        try:
            reward.name = reward_name
            reward.points_required = reward_point
            reward.save()

            child_ids = reward_childs.split(';')
            # Delete existing relation
            user_rewards = UserReward.objects.filter(reward=reward)
            if user_rewards:
                for user_reward in user_rewards:
                    user_reward.delete()
            # Insert new relation
            if len(child_ids) > 0 and child_ids[0] != '':
                for child_id in child_ids:
                    user_reward = UserReward()
                    user_reward.reward = reward
                    user_reward.user_id = long(child_id)
                    user_reward.save()

            return reward.id
        except Exception, e:
            logging.error("Update reward error, error is %s" % e)
            return None


    @staticmethod
    def delete_reward(reward_id):
        try:
            #args = {'reward': reward_id}
            #redemptions = Redemption.objects.filter(**args)
            #if redemptions:
            #    return False
            args = {'id': reward_id}
            reward = Reward.objects.get(**args)
            reward.is_deleted = True
            reward.save()
            return True
        except Exception:
            return False

class RedemptionManager(object):

    @staticmethod
    def redeem_reward(child, reward_id):
        try:
            redemption = Redemption()
            redemption.user = child
            redemption.reward = RewardsManager.get_reward_by_id(reward_id)
            redemption.created_at = datetime.datetime.today()
            redemption.save()
            return redemption.id
        except Exception:
            return None

    @staticmethod
    def get_redemption_by_user(child_id):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT r.name, rp.validated, r.points_required, rp.created_at\
                            FROM webverse_redemption rp, webverse_reward r where rp.user_id = %s and rp.reward_id = r.id \
                            and rp.id not in (SELECT id FROM webverse_redemption where  user_id = %s and validated = False)", [child_id,child_id])
            rewards = cursor.fetchall()
            result = []
            if rewards:
                for reward in rewards:
                    created_at = reward[3]
                    create_day = datetime.date(created_at.year, created_at.month, created_at.day)
                    today = datetime.date.today()
                    day = today - create_day
                    dict = {
                        'name': str(reward[0]),
                        'validated' :reward[1],
                        'points_required' : int(reward[2]),
                        'days': day.days,
                        'create_day': create_day
                    }
                    result.append(dict)
            return result
        except Exception:
            return None

    @staticmethod
    def get_redemption_by_parent_id(parent_id):
        args = {'parent_id' :parent_id, 'is_deleted' :False}
        args1 = {'validated': None}
        try:
            return Redemption.objects.filter(user__in=UserProfile.objects.filter(**args)).filter(**args1).order_by('validated').order_by('created_at')
        except Redemption.DoesNotExist:
            return None
        except Exception:
            return None

    @staticmethod
    def get_approved_redemption_by_parent_id(parent_id):
        args = {'parent_id' :parent_id}
        args1 = {'validated': None}
        try:
            return Redemption.objects.filter(user__in=UserProfile.objects.filter(**args)).exclude(**args1).order_by('-created_at')
        except Redemption.DoesNotExist:
            return None
        except Exception:
            return None

    @staticmethod
    def get_approved_redemption_by_kid_id(kid_id):
        args = {'user__id' :kid_id}
        args1 = {'validated': None}
        try:
            return Redemption.objects.filter(**args).exclude(**args1).order_by('-created_at')
        except Redemption.DoesNotExist:
            return None
        except Exception:
            return None

    @staticmethod
    @transaction.commit_on_success
    def reject_redemption(redemption_id):
        try:
            args = {'id': redemption_id}
            redemption = Redemption.objects.get(**args)
            redemption.validated = False
            redemption.validated_date = datetime.datetime.today()
            redemption.save()

            #Give reduced points back to child
#            child = redemption.user
#            child.points_balance = child.points_balance + redemption.reward.points_required
#            child.save()
            return redemption
        except Exception:
            return None

    @staticmethod
    def approve_redemption(redemption_id):
        try:
            args = {'id': redemption_id}
            redemption = Redemption.objects.get(**args)
            redemption.validated = True
            redemption.validated_date = datetime.datetime.today()
            redemption.save()
            return redemption
        except Exception:
            return None