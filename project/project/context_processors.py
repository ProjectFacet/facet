""" Context Processors for Facet.

    Passes along information to be available in all templates."""


from editorial.forms import PrivateMessageForm, UserNoteForm
from actstream.models import any_stream

def include_private_message_form(request):
    if request.user.is_authenticated():
        privatemessageform = PrivateMessageForm(request=request)
        usernoteform = UserNoteForm()
        return {'privatemessageform': privatemessageform, 'usernoteform': usernoteform}
    else:
        return {}

def include_activity_stream(request):
    if request.user.is_authenticated():
        activity_stream = any_stream(request.user)
        return {'activitystream': activity_stream }


# def include_user_note_form(request):
#     usernoteform = UserNoteForm()
#     print "USERNOTEFORM"
#     print usernoteform
#     return {'usernoteform': usernoteform}

# def include_private_message_form(request):
#     privatemessageform = PrivateMessageForm(request=request)
#     usernoteform = UserNoteForm()
#     return {'privatemessageform': privatemessageform, 'usernoteform': usernoteform}
