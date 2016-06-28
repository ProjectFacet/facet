""" Context Processors for Facet.

    Passes along information to be available in all templates."""


from editorial.forms import PrivateMessageForm, UserNoteForm

# def include_private_message_form(request):
#     privatemessageform = PrivateMessageForm(request=request)
#     usernoteform = UserNoteForm()
#     return {'privatemessageform': privatemessageform, 'usernoteform': usernoteform}

def include_private_message_form(request):
    if request.user.is_authenticated():
        privatemessageform = PrivateMessageForm(request=request)
        usernoteform = UserNoteForm()
        return {'privatemessageform': privatemessageform, 'usernoteform': usernoteform}
    else:
        return {}



# def include_user_note_form(request):
#     usernoteform = UserNoteForm()
#     print "USERNOTEFORM"
#     print usernoteform
#     return {'usernoteform': usernoteform}
