import pdb
import datetime

from jsonrpc import jsonrpc_method
from webverse.model.users import UserManager
from webverse.model.participation import ParticipationManager, ActivityManager


def my_auth(username, password):
    return UserManager.get_auth_user(username, password)
    
@jsonrpc_method('activity.report(activity_name=String, duration=Number, day=String) -> dict', authenticated=my_auth)
def post_activity(request, activity_name, duration, day):
    if request.user != None:
        activity_id = ActivityManager.get_activity_id_by_name(activity_name)
        if activity_id != None:
            # January 12, 2012 11:50:50 AM PST
            log_day = datetime.datetime.strptime(day,'%B %d, %Y %I:%M:%S %p')
            if log_day == None:
                return {'result' : False, 'error': 'bad log day'}
            # pdb.set_trace();
            user = UserManager.get_user_profile(request.user.id)
            if user == None:
                return {'result' : False, 'error': 'bad user profile', 'user_id' : request.user.id }
            participation_id = ParticipationManager.save_participation(activity_id, duration, log_day, user)
            if participation_id == None:
                return {'result' : False, 'error': 'no participation id'}
            return {'result' : True, 'activity_name': activity_name, 'duration' : duration, 'day' : log_day}
    return {'result': 0, 'error': 'not authenticated?' }        
    #return False
    
@jsonrpc_method('user.login() -> Boolean', authenticated=my_auth)
def login_user(request):
    # pdb.set_trace();
    if request.user != None:
        return True
    return False
