import logging
from django.db.models.aggregates import Count, Sum
from wjzpw.webverse.models import Activity, Participation, UserProfile, Badge, Achievement
import datetime
from django.db import connection, transaction
from django.shortcuts import get_object_or_404
from django.db.models import Q

class BadgeManager(object):

    @staticmethod
    def get_all_badges():
        try:
            return Badge.objects.all().order_by('name')
        except Badge.DoesNotExist:
            return None

    @staticmethod
    def get_badge_ids_by_child_id(child_id):
        try:
            return Achievement.objects.filter(user=child_id).defer('badge')
        except Achievement.DoesNotExist:
            return None

    @staticmethod
    def get_badge_tips(badges, badge_ids, child_id):
        tips_dict = {}
        for badge in badges:
            badge_id = badge.id
            if badge_id not in badge_ids:
                date_to = datetime.date.today()
                if badge.day_range is not None and badge.day_range != 0:
                    date_from = datetime.date.today() - datetime.timedelta(days=(badge.day_range-1))
                    args = {'user': child_id, 'validated': True, 'activity_date__range': (date_from, date_to) }
                else:
                    args = {'user': child_id, 'validated': True, 'activity_date__lte': date_to }
                if badge.activity is not None:
                    args['activity'] = badge.activity

                # Get already accepted participation
                participation_set = Participation.objects.filter(**args).order_by('activity_date')

                # day_rang is valid
                if badge.day_range is not None and badge.day_range != 0:
                    BadgeManager.get_badge_tip_day_rang(tips_dict, badge, participation_set)

                # day_rang is invalid
                else:
                    BadgeManager.get_badge_tip_no_day_rang(tips_dict, badge, participation_set)

        return tips_dict

    @staticmethod
    def get_badge_tip_day_rang(tips_dict, badge, participation_set):
        date_from = datetime.date.today() - datetime.timedelta(days=(badge.day_range-1))
        date_to = datetime.date.today()
        date_cursor = date_from

        while date_cursor <= date_to:
            left_days = (date_cursor - date_from).days
            #total_minutes = 0
            total_times = 0
            # temp->current consecutive times, maxValue-> max consecutive times in the rang days, temp_minutes->total minutes of current day
            maxValue,temp,temp_minutes = 0,0,0
            is_consecutive = False
            last_date = None
            if participation_set:
                maxValue = 1
            for participation in participation_set:
                if date_cursor <= participation.activity_date <= date_to:
                    if last_date is None:
                        last_date = participation.activity_date
                        #total_minutes += participation.duration_minute
                    total_times += 1
                    if last_date == participation.activity_date:
                        temp_minutes += participation.duration_minute
                        continue
                    elif (last_date + datetime.timedelta(days=1)) == participation.activity_date:
                        if badge.duration_minute is None or badge.duration_minute == 0 or temp_minutes >= badge.duration_minute:
                            temp += 1
                            if temp > maxValue:
                                maxValue = temp
                    else:
                        temp = 0
                    temp_minutes = participation.duration_minute
                    last_date = participation.activity_date
            if last_date == date_to:
                is_consecutive = True
                # for the last participation
            if badge.duration_minute is None or badge.duration_minute == 0:
                temp += 1
                if temp > maxValue:
                    maxValue = temp
            else:
                if temp_minutes >= badge.duration_minute:
                    temp += 1
                    if temp > maxValue:
                        maxValue = temp
                # Statistics duration minutes
            #temp_seconds = (datetime.datetime.strptime(str(datetime.date.today() + datetime.timedelta(days=1)), '%Y-%m-%d') - datetime.datetime.today()).seconds
            #tmp_minutes = temp_seconds/60 + left_days*24*60
            #if badge.duration_minute is not None and badge.duration_minute != 0 and tmp_minutes + total_minutes < badge.duration_minute:
            #    date_cursor += datetime.timedelta(days=1)
            #    continue

            # Statistics continuous days
            if is_consecutive:
                already_days = temp
            else:
                already_days = 0
            if badge.consecutive_count is not None and badge.consecutive_count != 0 and maxValue < badge.consecutive_count and left_days + 1 + already_days < badge.consecutive_count:
                date_cursor += datetime.timedelta(days=1)
                continue;

            # Return statistics info
            if badge.activity is None:
                msg = 'You need to participate in any activity'
            else:
                msg = 'You need to participate in ' + badge.activity.name
                #if badge.duration_minute is not None and badge.duration_minute != 0:
            #    diff_minutes = badge.duration_minute - total_minutes
            #    if diff_minutes > 0:
            #        msg += ' for a total of ' + str(diff_minutes) + ' minutes, '

            if badge.participation_count is not None and badge.participation_count != 0:
                diff_times = badge.participation_count - total_times
                if diff_times > 0:
                    msg += ' for ' + str(diff_times) + ' times'

            if badge.consecutive_count is not None and badge.consecutive_count != 0 and maxValue < badge.consecutive_count:
                msg += ', continuously for ' + str(badge.consecutive_count - already_days) + ' days in the next ' + str(left_days+1) +' days (include today)'

            if badge.duration_minute is not None and badge.duration_minute != 0:
                msg += ', more than ' + str(badge.duration_minute) + ' minutes a day'
            tips_dict[badge.id] = msg
            break;

    @staticmethod
    def get_badge_tip_no_day_rang(tips_dict, badge, participation_set):
        BadgeManager.process_badge_tip(tips_dict, badge, participation_set)

    @staticmethod
    def process_badge_tip(tips_dict, badge, participation_set):
        #total_minutes = 0
        total_times = 0
        # maxValue->max consecutive times in the rang days, temp->current consecutive times, temp_minutes->total minutes in current day
        maxValue,temp, temp_minutes = 0,0,0
        last_date = None
        if participation_set:
            maxValue = 1
        for participation in participation_set:
            if last_date is None:
                last_date = participation.activity_date
                #total_minutes += participation.duration_minute
            total_times += 1
            if last_date == participation.activity_date:
                temp_minutes += participation.duration_minute
                continue
            elif (last_date + datetime.timedelta(days=1)) == participation.activity_date:
                if badge.duration_minute is None or badge.duration_minute == 0 or temp_minutes >= badge.duration_minute:
                    temp += 1
                    if temp > maxValue:
                        maxValue = temp
            else:
                temp = 0
            temp_minutes = participation.duration_minute
            last_date = participation.activity_date
            # for the last participation
        if badge.duration_minute is None or badge.duration_minute == 0:
            temp += 1
            if temp > maxValue:
                maxValue = temp
        else:
            if temp_minutes >= badge.duration_minute:
                temp += 1
                if temp > maxValue:
                    maxValue = temp

        # Return statistics info
        if badge.activity is None:
            msg = 'You need to participate in any activity'
        else:
            msg = 'You need to participate in ' + badge.activity.name
            #if badge.duration_minute is not None and badge.duration_minute != 0:
        #   diff_minutes = badge.duration_minute - total_minutes
        #    if diff_minutes > 0:
        #        msg += ' for a total of ' + str(diff_minutes) + ' minutes, '

        if badge.participation_count is not None and badge.participation_count != 0:
            diff_times = badge.participation_count - total_times
            if diff_times > 0:
                msg += ' for ' + str(diff_times) + ' times'

        if badge.consecutive_count is not None and badge.consecutive_count != 0 and maxValue < badge.consecutive_count:
            # TODO: [winston] Commented out to be fixed.
            #if left_days+1 >= badge.consecutive_count:
            #    msg += ' for ' + str(badge.consecutive_count) + ' consecutive days'
            #else:
            msg += ', continuously for ' + str(badge.consecutive_count) + ' days'
        if badge.duration_minute is not None and badge.duration_minute != 0:
            msg += ', more than ' + str(badge.duration_minute) + 'minutes a day'
        tips_dict[badge.id] = msg

class ActivityManager(object):

    @staticmethod
    def get_all_activities():
        try:
            activities = Activity.objects.all().order_by('name')
            return activities
        except Activity.DoesNotExist:
            return None

    @staticmethod
    def get_activity_by_id(activity_id):
        try:
            return Activity.objects.get(pk=activity_id)
        except Activity.DoesNotExist:
            return None
            
    @staticmethod
    def get_activity_id_by_name(activity_name):
        try:
            args = {"name" :activity_name }
            activity = Activity.objects.get(**args)
            return activity.id
        except Activity.DoesNotExist:
            return None

class ParticipationManager(object):

    @staticmethod
    def get_participation_by_parent_id(parent_id):
        args = {"parent_id" :parent_id, "is_deleted": False}
        try:
            return Participation.objects.filter(user__in=UserProfile.objects.filter(**args)).order_by('-activity_date')
        except Participation.DoesNotExist:
            return None


    @staticmethod
    def get_participation_by_id(participation_id):
        participation = Participation.objects.get(pk=participation_id)
        return participation

    @staticmethod
    @transaction.commit_on_success
    def approve_participation(part_id):
        args = {'id': part_id}
        participation = Participation.objects.get(**args)
        participation.validated = True
        participation.save()

        # Update child - badge relation
        return ParticipationManager.update_badges(participation)

    @staticmethod
    def update_badges(participation):
        # Update child - badge relation
        #args = {"activity" :participation.activity}
        badges = Badge.objects.filter(Q(activity=participation.activity) | Q(activity=None))
        if badges:
            for badge in badges:
                if badge.day_range is not None and badge.day_range != 0:
                    # query approved participation which is in scope (participation.activity_date +- (badge.day_range-1))
                    date_from = participation.activity_date - datetime.timedelta(days=(badge.day_range-1))
                    while date_from <= participation.activity_date:
                        if ParticipationManager.update_badges_check(participation, badge, date_from, (date_from + datetime.timedelta(days=(badge.day_range-1)))):
                            break
                        date_from = date_from + datetime.timedelta(days=(badge.day_range-1))
                else:
                    # query all approved participation
                    ParticipationManager.update_badges_check(participation, badge, None, None)

        return participation

    @staticmethod
    def update_badges_check(participation, badge, day_start, day_end):
        if day_start is not None and day_end is not None:
            # query approved participation which is in scope day_start and day_end
            args = {'user': participation.user, 'validated': True, 'activity_date__range': (day_start, day_end) }
        else:
            # query all approved participation
            args = {'user': participation.user, 'validated': True}
        if badge.activity is not None:
            args['activity'] = badge.activity

        #### check participation_count
        #sum_minute = Participation.objects.filter(**args).aggregate(Sum('duration_minute'))
        count_participation = Participation.objects.filter(**args).aggregate(Count('id'))

        # temp->current consecutive times, maxValue-> max consecutive times in the rang days, temp_minutes->total minutes of current day
        temp,maxValue,temp_minutes = 0,0,0
        participation_set = Participation.objects.filter(**args).order_by('activity_date')

        #### check consecutive_count and duration_minute
        date_last = None
        if participation_set:
            for temp_participation in participation_set:
                if date_last is None:
                    date_last = temp_participation.activity_date
                if temp_participation.activity_date == date_last:
                    temp_minutes += temp_participation.duration_minute
                    continue
                elif (date_last + datetime.timedelta(days=1)) == temp_participation.activity_date:
                    if badge.duration_minute is None or badge.duration_minute == 0 or temp_minutes >= badge.duration_minute:
                        temp += 1
                        if temp > maxValue:
                            maxValue = temp
                else:
                    temp = 0
                temp_minutes = temp_participation.duration_minute
                date_last = temp_participation.activity_date
                # for the last participation
            if badge.duration_minute is None or badge.duration_minute == 0:
                temp += 1
                if temp > maxValue:
                    maxValue = temp
            else:
                if temp_minutes >= badge.duration_minute:
                    temp += 1
                    if temp > maxValue:
                        maxValue = temp

        #if (badge.duration_minute is None or badge.duration_minute == 0 or sum_minute >= badge.duration_minute) and (badge.participation_count is None or badge.participation_count == 0 or count_participation >= badge.participation_count) and (badge.consecutive_count is None or badge.consecutive_count == 0 or maxValue >= badge.consecutive_count):
        if (badge.participation_count is None or badge.participation_count == 0 or count_participation >= badge.participation_count) and (badge.consecutive_count is None or badge.consecutive_count == 0 or maxValue >= badge.consecutive_count):
            args = {'user': participation.user, 'badge': badge}
            try:
                Achievement.objects.get(**args)
            except Achievement.DoesNotExist:
                achievement = Achievement()
                achievement.user = participation.user
                achievement.badge = badge
                achievement.created_at = datetime.datetime.today()
                achievement.save()
            finally:
                return True
        else:
            return False

    @staticmethod
    def reject_participation(part_id):
        try:
            args = {'id': part_id}
            participation = Participation.objects.get(**args)
            participation.validated = False
            participation.save()
            return participation
        except Exception:
            return None

    @staticmethod
    def save_participation(activity_id, time, date, user):
        try:
            participation = Participation()
            activity = ActivityManager.get_activity_by_id(activity_id)
            points_reward = (activity.points_per_minute) * int(time)
            participation.points_awarded = points_reward
            participation.user = user
            participation.activity = activity
            participation.validated = None
            participation.duration_minute = time
            participation.activity_date = date
            participation.created_at = datetime.datetime.today()
            participation.save()
            return participation.id
        except Exception:
            return None

    @staticmethod
    @transaction.commit_on_success
    def save_participation_by_kids_id(activity_id, time, date, kid_id):
        try:
            kid = get_object_or_404(UserProfile, id=kid_id)
            participation = Participation()
            activity = ActivityManager.get_activity_by_id(activity_id)
            points_reward = (activity.points_per_minute) * int(time)
            participation.points_awarded = points_reward
            participation.user = kid
            participation.activity = activity
            participation.validated = True
            participation.duration_minute = time
            participation.activity_date = date
            participation.created_at = datetime.datetime.today()
            participation.save()

            # Update child - badge relation
            participation  = ParticipationManager.update_badges(participation)
            return participation.id
        except Exception, e:
            logging.error("Create participation for kid error, error is %s" % e)
            return None


    @staticmethod
    def update_participation_by_id(participation, child_id, activity_id, duration_minute, activity_date, real_date):
        try:
            activity = ActivityManager.get_activity_by_id(activity_id)
            points_reward = (activity.points_per_minute) * int(duration_minute)
            participation.user_id = child_id
            participation.activity_id = activity_id
            participation.duration_minute = duration_minute
            participation.activity_date = real_date
            participation.points_awarded = points_reward
            participation.save()
            return participation.id
        except Exception, e:
            logging.error("Update participation error, error is %s" % e)
            return None


    @staticmethod
    def get_stats_by_child_id(child_id, today):
        """Return child's activity times by child_id.
        """
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT sum(duration_minute) as duration, activity_date as date FROM webverse_participation \
                        where user_id = %s and validated = True and activity_date <= %s\
                        group by activity_date order by activity_date asc", [int(child_id),today])
            stats = cursor.fetchall()
            result = []
            if stats:
                for stat in stats:
                    dict = {
                        'duration': str(stat[0]),
                        'date': str(stat[1])
                    }
                    result.append(dict)
            return result
        except Exception:
            return None

    @staticmethod
    def get_activities_by_child_id(child_id, today):
        """Return child's activity times by child_id.
        """
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT duration_minute as duration, activity_date as date, validated, id FROM webverse_participation \
                        where user_id = %s and activity_date <= %s\
                        order by activity_date asc", [int(child_id),today])
            stats = cursor.fetchall()
            result = []
            if stats:
                for stat in stats:
                    participation = ParticipationManager.get_participation_by_id(stat[3])
                    activity = participation.activity
                    dict = {
                        'duration': str(stat[0]),
                        'date': str(stat[1]),
                        'validated': str(stat[2]),
                        'id': str(stat[3]),
                        'activity': str(activity.name)
                    }
                    result.append(dict)
            return result
        except Exception:
            assert False
            return None

    @staticmethod
    def get_total_points_award(child_id):
        """Return child's total point_award he ever got.
        """
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT sum(points_awarded) as point FROM webverse_participation \
                        where user_id = %s and validated = True", [child_id])
            result = cursor.fetchone()
            if result == None or result[0] == None:
                return 0
            else:
                return result[0]
        except Exception:
            return None

    @staticmethod
    def get_used_points_award(child_id):
        """Return child's used point_award he ever paid.
        """
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT sum(rd.points_required) as point FROM webverse_redemption rp, webverse_reward rd \
                        where rp.reward_id = rd.id and rp.user_id = %s and rp.id not in (select rp1.id from webverse_redemption rp1 where rp1.validated = False)", [child_id])
            result = cursor.fetchone()
            if result == None or result[0] == None:
                return 0
            else:
                return result[0]
        except Exception:
            return 0

    @staticmethod
    def get_current_points(child_id):
        """Return child's current point_award he can use.
        """
        try:
            total_points = ParticipationManager.get_total_points_award(child_id)
            used_points = ParticipationManager.get_used_points_award(child_id)
            current_points = int(total_points) - int(used_points)
            return current_points
        except Exception:
            return None