from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import loader
from django.template.context import RequestContext
from metaverse import settings
from metaverse.webverse.model.participation import ActivityManager, ParticipationManager, BadgeManager
import datetime
from metaverse.webverse.model.rewards import RewardsManager,RedemptionManager
from django.http import HttpResponse, HttpResponseRedirect
from metaverse.webverse.utils import send_email
from metaverse.webverse import utils
from metaverse.webverse.model.users import UserManager

kid_home_page = "../views/kid/kid.html"
kid_stats_page = "../views/kid/stats.html"
kid_badges_page = "kid/badges.html"
kid_rewards_page = "kid/rewards.html"
GOLD_STAR_MIN = settings.GOLD_STAR_MIN

@login_required
def kid(request):
    user = request.user.get_profile()
    points = ParticipationManager.get_current_points(user.id)
    activities = ActivityManager.get_all_activities()
    return render_to_response(kid_home_page, {}, RequestContext(request, {
            'activities':activities,
            'points':points,
        }),
    )

@login_required
def add_activity(request):
    """Child submit his own participation.
    """
    is_success = False
    activities = ActivityManager.get_all_activities()
    user = request.user.get_profile()
    points = ParticipationManager.get_current_points(user.id)
    if request.method == 'POST':

        activity_id = request.POST.get('activity-selector', '')
        time = request.POST.get('time-selector', '')
        date = request.POST.get('date-selector', '')
        real_date = datetime.datetime.today() - datetime.timedelta(int(date))
        participation = ParticipationManager.save_participation(activity_id, time, real_date, user)
        if participation:
            is_success = True

    return HttpResponse(is_success)
#    return render_to_response(kid_home_page, {},
#        RequestContext(request, {
#            'activities':activities,
#            'is_success':is_success,
#            'points':points,
#        }),
#    )


# Nav to badges page
@login_required
def badges(request):
    child_id = request.user.get_profile().id

    badges = BadgeManager.get_all_badges()
    badge_ids = [achievement.badge_id for achievement in BadgeManager.get_badge_ids_by_child_id(child_id)]
    # Tips of how to get badge
    badge_tips = BadgeManager.get_badge_tips(badges, badge_ids, child_id)

    badges_page = loader.get_template(kid_badges_page).name
    points = ParticipationManager.get_current_points(child_id)
    return render_to_response(badges_page, RequestContext(request, {
        'badges': badges,
        'badge_ids': badge_ids,
        'points':points,
        'badge_tips':badge_tips
    }))

@login_required
def kid_stats(request):
    """Show the child's exercise stats.
    """
    user = request.user.get_profile()
    today = datetime.date.today()
    stats = ParticipationManager.get_stats_by_child_id(user.id, today)
    activities = ParticipationManager.get_activities_by_child_id(user.id, today)
    points = ParticipationManager.get_current_points(user.id)
    redemptions = RedemptionManager.get_redemption_by_user(user.id)
    return render_to_response(kid_stats_page, {},
        RequestContext(request,{
            'stats':stats,
            'points':points,
	        'redemptions': redemptions,
			'activities': activities,
            'GOLD_STAR_MIN':GOLD_STAR_MIN
        }),
    )

@login_required
def kid_rewards(request):
    user = request.user.get_profile()
    points = ParticipationManager.get_current_points(user.id)
    rewards = RewardsManager.get_rewards_by_child_id(user.id, points)
    redemptions = RedemptionManager.get_redemption_by_user(user.id)
    past_redemptions = RedemptionManager.get_approved_redemption_by_kid_id(user.id)
    return render_to_response(kid_rewards_page, RequestContext(request,{
        'points': points,
        'rewards' : rewards,
        'redemptions': redemptions,
        'past_redemptions': past_redemptions
    }))

@login_required
def kid_redeem_reward(request):
    """
    1. Get reward required points
    2. Get kid current points and check if the kids can redeem the rewards
    """
    is_success = False

    user = request.user.get_profile()
    #Get reward required points and kid current point
    reward_id = request.POST.get('hidden_reward_id', '')
    reward_point = request.POST.get('hidden_reward_point', '')
    kid_point = ParticipationManager.get_current_points(user.id)
    if(reward_id and reward_point):
        if(not ((utils.intvalue(kid_point) - utils.intvalue(reward_point)) < 0)):
            if RedemptionManager.redeem_reward(user, reward_id):
                is_success = True

    #Reload rewards and redemptions
    rewards = RewardsManager.get_rewards_by_child_id(user.id, kid_point)
    redemptions = RedemptionManager.get_redemption_by_user(user.id)

    return HttpResponseRedirect("/kid/rewards/")
#    return render_to_response(kid_rewards_page, RequestContext(request,{
#            'points': kid_point,
#            'rewards' : rewards,
#            'is_success': is_success,
#            'redemptions': redemptions,
#        }))

@login_required
def kid_remind_parent(request):
    user = request.user.get_profile()
    send_mail_success = False
    parent_id = user.parent_id
    parent = UserManager.get_user_profile(parent_id)
    reward_name = request.GET.get('reward_name', '')
    if user.gender is 1:
        send_mail_success = send_email((utils.remind_parent_mail_template_girl % (parent.username, user.username, reward_name)), parent.email, u'Your Kid Remind')
    else:
        send_mail_success = send_email((utils.remind_parent_mail_template_boy % (parent.username, user.username, reward_name)), parent.email, u'Your Kid Remind')
    return HttpResponse(send_mail_success)