import datetime
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import loader
from django.template.context import RequestContext
from wjzpw import settings
from wjzpw.webverse.forms.forms import KidsForm, ChangeEmailForm, KidsEditForm, PasswordReset
from wjzpw.webverse.model.participation import ParticipationManager, ActivityManager, BadgeManager
from wjzpw.webverse.model.rewards import SuggestionRewardManager, RedemptionManager, RewardsManager
from wjzpw.webverse.model.users import UserManager
from wjzpw.webverse.models import UserProfile
from django.template.loader import render_to_string

parent_inbox_page = 'parent/inbox.html'
parent_rewards_page = 'parent/rewards.html'
parent_badges_page = 'parent/badges.html'
parent_settings_page = 'parent/settings.html'
parent_change_email_page = 'parent/change_email.html'
parent_change_password_page = 'parent/change_password.html'
parent_add_kids_page = 'parent/add_kids.html'
parent_manage_kids_page = 'parent/manage_kids.html'
parent_edit_kids_page = 'parent/edit_kids.html'
parent_stats_page = 'parent/stats.html'
settings_page = 'parent/settings.html'
GOLD_STAR_MIN = settings.GOLD_STAR_MIN

@login_required
def inbox(request):
    user_profile = request.user.get_profile()
    parent_id = user_profile.id
    participation_list = ParticipationManager.get_participation_by_parent_id(parent_id)
    redemptions = RedemptionManager.get_redemption_by_parent_id(parent_id)

    # Load activity list in system
    activity_list = ActivityManager.get_all_activities()
    inbox_page = loader.get_template(parent_inbox_page).name
    #Get all kids by parent id
    kids = UserManager.get_children_by_parent(user_profile)
    return render_to_response(inbox_page, RequestContext(request,
            {
                "participation_list": participation_list,
                "activity_list": activity_list,
                "kids": kids,
                "redemptions": redemptions
            }))


@login_required
def add_activity(request):
    """Add activity for kids
    """
    is_success = False
    if request.method == 'POST':

        kid_id = request.POST.get('kids-selector', '')
        activity_id = request.POST.get('activity-selector', '')
        time = request.POST.get('time-selector', '')
        date = request.POST.get('date-selector', '')
        real_date = datetime.datetime.today() - datetime.timedelta(int(date))
        participation = ParticipationManager.save_participation_by_kids_id(activity_id, time, real_date, kid_id)
        if participation:
            is_success = True
    return HttpResponse(is_success)

@login_required
def edit_activity(request):
    """Add activity for kids
    """
    is_success = False
    if request.method == 'GET':
        participation_id = request.GET.get('participation_id', '')
        participation = ParticipationManager.get_participation_by_id(participation_id)
        if participation == '':
            is_success = False
        else:
            try:
                child_id = request.GET.get('child_id', '')
                activity_id = request.GET.get('activity_id', '')
                duration_minute = request.GET.get('duration_minute', '')
                activity_date = request.GET.get('activity_date', '')
                real_date = datetime.datetime.today() - datetime.timedelta(int(activity_date))
                participation = ParticipationManager.update_participation_by_id(participation, child_id, activity_id, duration_minute, activity_date, real_date)
                if participation:
                    is_success = True
            except Exception, e:
                is_success = False
    return HttpResponse(is_success)

# Approve participation
@login_required
def approve(request, part_id):
    try:
        part_id = long(part_id)
    except ValueError:
        raise Http404

    ParticipationManager.approve_participation(part_id)
    return redirect('/parent/inbox/')


# Reject participation
@login_required
def reject(request, part_id):
    try:
        part_id = long(part_id)
    except ValueError:
        raise Http404

    ParticipationManager.reject_participation(part_id)
    return redirect('/parent/inbox/')


# Approve redemption
@login_required
def approve_redemption(request, redemption_id, type):
    try:
        redemption_id = long(redemption_id)
    except ValueError:
        raise Http404

    RedemptionManager.approve_redemption(redemption_id)
    if type == '1':
        return redirect('/parent/rewards/')
    else:
        return redirect('/parent/inbox/')


# Reject redemption
@login_required
def reject_redemption(request, redemption_id, type):
    try:
        redemption_id = long(redemption_id)
    except ValueError:
        raise Http404

    RedemptionManager.reject_redemption(redemption_id)
    if type == '1':
        return redirect('/parent/rewards/')
    else:
        return redirect('/parent/inbox/')


# Nav to badges page
@login_required
def badges(request, child_id):
    user_profile = request.user.get_profile()
    childs = UserManager.get_childs_by_parent_id(user_profile.id)
    if child_id == '0' and childs:
        child_id = childs[0].id

    badges = BadgeManager.get_all_badges()
    badge_ids = [achievement.badge_id for achievement in BadgeManager.get_badge_ids_by_child_id(child_id)]
    # Tips of how to get badge
    badge_tips = BadgeManager.get_badge_tips(badges, badge_ids, child_id)

    badges_page = loader.get_template(parent_badges_page).name
    return render_to_response(badges_page, RequestContext(request, {
        'childs': childs,
        'badges': badges,
        'badge_ids': badge_ids,
        'child_id':int(child_id),
        'badge_tips':badge_tips
    }))

# Nav to rewards page
@login_required
def rewards(request):
    user_profile = request.user.get_profile()
    parent_id = user_profile.id
    success = request.META.get('success', None)

    redemptions = RedemptionManager.get_redemption_by_parent_id(parent_id)
    past_redemptions = RedemptionManager.get_approved_redemption_by_parent_id(parent_id)
    rewards = RewardsManager.get_reward_by_parent_id(parent_id)
    suggest_rewards = SuggestionRewardManager.get_all_suggestion_rewards()
    childs = UserManager.get_childs_by_parent_id(parent_id)

    rewards_page = loader.get_template(parent_rewards_page).name
    return render_to_response(rewards_page, RequestContext(request, {
        'suggest_rewards': suggest_rewards,
        'redemptions': redemptions,
        'rewards': rewards,
        'childs': childs,
        'success': success,
        'past_redemptions': past_redemptions
    }))

# Delete reward
@login_required
def delete_reward(request, reward_id):
    try:
        reward_id = long(reward_id)
    except ValueError:
        raise Http404

    request.META['success'] = RewardsManager.delete_reward(reward_id)
    return rewards(request)

# Add reward
@login_required
def add_reward(request):
    is_success = False
    if request.method == 'POST':
        parent_id = request.user.get_profile().id
        reward_name = request.POST.get('reward_name', '')
        reward_point = request.POST.get('reward_point', '')
        reward_childs = request.POST.get('reward_childs', '')
        reward = RewardsManager.save_reward(parent_id, reward_name, reward_point, reward_childs)
        if reward:
            is_success = True
    return HttpResponse(is_success)


# Edit reward
@login_required
def edit_reward(request):
    is_success = False
    if request.method == 'GET':
        parent_id = request.user.get_profile().id
        reward_id = request.GET.get('reward_id', '')

        reward = RewardsManager.get_reward_by_id(reward_id)
        if reward == '':
            is_success = False
        else:
            reward_name = request.GET.get('reward_name', '')
            reward_point = request.GET.get('reward_point', '')
            reward_childs = request.GET.get('reward_childs', '')
            reward = RewardsManager.edit_reward(reward, reward_name, reward_point, reward_childs)
            if reward:
                is_success = True
    return HttpResponse(is_success)

@login_required
def stats(request):
    """Return each child's stats.
    """
    parent = request.user.get_profile()
    children = UserManager.get_children_by_parent(parent)
    today = datetime.date.today()
    stats = None
    child_id = None
    points = None
    activities = None
    redemptions = None
    if children:
        child_id = children[0].id
        stats = ParticipationManager.get_stats_by_child_id(child_id, today)
        activities = ParticipationManager.get_activities_by_child_id(child_id, today)
        points = ParticipationManager.get_current_points(child_id)
        redemptions = RedemptionManager.get_redemption_by_user(child_id)
    
    return render_to_response(parent_stats_page, {},
        RequestContext(request, {
            'children': children,
            'child_id': child_id,
            'stats': stats,
            'points':points,
            'redemptions': redemptions,
            'activities': activities,
            'GOLD_STAR_MIN':GOLD_STAR_MIN
        })
    )

@login_required
def get_stats_by_child(request):
    child_id = request.POST.get('hidden_id','')
    parent = request.user.get_profile()
    children = UserManager.get_children_by_parent(parent)
        
    today = datetime.date.today()
    stats = None
    activities = None
    points = None
    redemptions = None
    
    if child_id:
        stats = ParticipationManager.get_stats_by_child_id(child_id, today)
        activities = ParticipationManager.get_activities_by_child_id(child_id, today)
        points = ParticipationManager.get_current_points(child_id)
        redemptions = RedemptionManager.get_redemption_by_user(child_id)
    
    return render_to_response(parent_stats_page, {},
        RequestContext(request, {
            'children': children,
            'child_id': child_id,
            'stats':stats,
            'points':points,
            'redemptions': redemptions,
            'activities': activities,
            'GOLD_STAR_MIN':GOLD_STAR_MIN
        })
    )

@login_required
def manage_change_email(request):
    return render_to_response(parent_settings_page, RequestContext(request, {
        "change_email" : change_email(request),
        "operate":'email'
    }))

#redirect change Email page
@login_required
def change_email(request):
    user_profile         = request.user.get_profile()
    changeEmailForm      = ChangeEmailForm(request.user, user_profile)
    change_email_success = False
    if request.method == 'POST':
        changeEmailForm = ChangeEmailForm(request.user, user_profile, request.POST)
        if changeEmailForm.is_valid():
                user = changeEmailForm.save(changeEmailForm.cleaned_data)
                if user:
                    change_email_success = True
    result = render_to_string(parent_change_email_page, RequestContext(request, {
            'change_email_success':change_email_success,
            'changeEmailForm':changeEmailForm
        })
    )
    return result

@login_required
def manage_change_password(request):
    return render_to_response(parent_settings_page, RequestContext(request, {
        "change_password" : change_password(request),
        "operate":'password'
    }))

@login_required
def change_password(request):
    passwordresetForm = PasswordReset(request.user)
    change_password_success = False
    if request.method == 'POST':
        passwordresetForm = PasswordReset(request.user, request.POST)
        if passwordresetForm.is_valid():
            user = request.user
            user.set_password(passwordresetForm.cleaned_data['password1'])
            user.save()
            change_password_success = True
    result = render_to_string(parent_change_password_page, RequestContext(request, {
            'change_password_success':change_password_success,
            'passwordresetForm':passwordresetForm,
        })
    )
    return result

@login_required
def manage_kids(request, kid = None):
    return render_to_response(parent_settings_page, RequestContext(request, {
        "manage_kids" : show_kids(request, kid),
        "operate":'manage',
    }))

@login_required
def show_kids(request, kid):
    delete_kid_success = False
    if kid:
        delete_kid_success = UserManager.delete_kid_profile(kid)
    user_profile = request.user.get_profile()
    userProfile_list = UserProfile.objects.all().filter(parent_id = user_profile.id, is_deleted = False).order_by('updated_at')
    result = render_to_string(parent_manage_kids_page, RequestContext(request, {
            'userProfile_list':userProfile_list,
            "delete_kid_success":delete_kid_success
        })
    )
    return result

@login_required
def manage_update_kids(request, k_id=None):
    return render_to_response(parent_settings_page, RequestContext(request, {
            "update_kids" : update_kids(request, k_id),
            "operate":'manage',
            })
        )

@login_required
def update_kids(request, k_id):
    update_kid_success = False
    user_profile = request.user.get_profile()
    kid_profile = UserProfile.objects.filter(id = k_id)
    data = {
        'u_username':kid_profile[0].user.username,
        'u_realname':kid_profile[0].realname,
        'u_password':kid_profile[0].user.password,
        'u_gender':kid_profile[0].gender,
        'u_birthday':kid_profile[0].birthdate,
        'u_kid_id':kid_profile[0].id,
    }
    kidsEditForm = KidsEditForm(data)
    if request.method == 'POST':
        kidsEditForm = KidsEditForm(request.POST)
        if kidsEditForm.is_valid():
            if user_profile:
                kid = kidsEditForm.save(kidsEditForm.cleaned_data)
                if kid:
                    update_kid_success = True
    result = render_to_string(parent_edit_kids_page, RequestContext(request, {
            'update_kid_success':update_kid_success,
            'kidsEditForm':kidsEditForm
        })
    )
    return result

@login_required
def settings(request):
    return render_to_response(parent_settings_page, {}, RequestContext(request,
            {
                "add_kids" : add_kids(request),
                "operate":'add'
            }))

@login_required
def add_kids(request):
    user_profile  = request.user.get_profile()
    add_kid_success = False
    kidsForm = KidsForm()
    if request.method == 'POST':
        kidsForm = KidsForm(request.POST)
        if kidsForm.is_valid():
            if user_profile:
                kidsForm.save(kidsForm.cleaned_data, user_profile.id)
                add_kid_success = True
                kidsForm = KidsForm()
    result = render_to_string(parent_add_kids_page, RequestContext(request, {
            'add_kid_success':add_kid_success,
            'kidsForm':kidsForm
        })
    )
    return result


