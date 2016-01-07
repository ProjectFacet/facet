""" Context Processors for Facet.

    Passes along information to be available in all templates."""


from editorial.forms import PrivateMessageForm

def include_private_message_form(request):
    privatemessageform = PrivateMessageForm()
    return {'privatemessageform': privatemessageform}
