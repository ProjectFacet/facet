""" Context Processors for Facet.

    Passes along information to be available in all templates."""


from editorial.forms import PrivateMessageForm, NoteForm
from actstream.models import any_stream, model_stream
from editorial.models import Organization, User
from django.contrib.sessions.models import Session
from django.utils import timezone

def include_private_message_form(request):
    return {}
    if request.user.is_authenticated():
        privatemessageform = PrivateMessageForm(request=request)
        usernoteform = NoteForm()
        return {'privatemessageform': privatemessageform, 'usernoteform': usernoteform}
    else:
        return {}

def include_activity_stream(request):
    return {}
    if request.user.is_authenticated():
        activity_stream = model_stream(request.user)
        return {'activitystream': activity_stream }
    else:
        return {}

def include_logged_in_users(request):
    if request.user.is_authenticated():
        active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        user_id_list = []
        for session in active_sessions:
            data = session.get_decoded()
            user_id_list.append(data.get('_auth_user_id', None))
        # Query all logged in users based on id list
        current_users = User.objects.filter(id__in=user_id_list)
        if request.user.organization:
            org_users = Organization.get_org_users(request.user.organization)
        else:
            org_users = []
        return {'org_users': org_users,
                'current_users': current_users}
    else: return {}


# def include_current_users(request):
#     active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
#     user_id_list = []
#     for session in active_sessions:
#         data = session.get_decoded()
#         user_id_list.append(data.get('_auth_user_id', None))
#     # Query all logged in users based on id list
#     current_users = User.objects.filter(id__in=user_id_list)
#     return current_users


# def include_user_note_form(request):
#     usernoteform = UserNoteForm()
#     print "USERNOTEFORM"
#     print usernoteform
#     return {'usernoteform': usernoteform}

# def include_private_message_form(request):
#     privatemessageform = PrivateMessageForm(request=request)
#     usernoteform = UserNoteForm()
#     return {'privatemessageform': privatemessageform, 'usernoteform': usernoteform}
