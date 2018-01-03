from .models import ContractorProfile, TalentEditorProfile


class FacetInfoMiddleware(object):
    """Adds commonly-needed things to request.

    Adds:
    - org: organization for user (or None)
    - is_contractor: T/F if user is contractor
    - is_talenteditor: T/F if talent editor
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if user.is_authenticated:
            request.org = user.organization
            request.is_contractor = ContractorProfile.objects.filter(user=user).exists()
            request.is_talenteditor = TalentEditorProfile.objects.filter(user=user).exists()
        else:
            request.org = None
            request.is_contractor = False
            request.is_talenteditor = False

        response = self.get_response(request)

        return response
