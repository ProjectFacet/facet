import time

from .models import ContractorProfile, TalentEditorProfile


class FacetInfoMiddleware(object):
    """Adds commonly-needed things to request.

    Adds:
    - org: organization for user (or None)
    - is_contractor: T/F if user is contractor
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.org = request.user.organization
            request.is_contractor = ContractorProfile.objects.filter(user=request.user).exists()
            request.is_talenteditor = TalentEditorProfile.objects.filter(user=request.user).exists()
        else:
            request.org = None
            request.is_contractor = False

        response = self.get_response(request)

        return response
