from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView, FormView, UpdateView, DetailView, ListView, DeleteView, TemplateView, View
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.conf import settings
from actstream import action
from editorial.models import Story
from braces.views import LoginRequiredMixin, FormMessagesMixin
from editorial.views import CustomUserTest
from django.db.models import Q

from ..models import Facet, FacetTemplate, Organization
from ..forms import (
    FacetTemplateForm,
    get_facet_form_for_template,
    FacetPreCreateForm,
    CommentForm,
    ImageAssetForm,
    DocumentAssetForm,
    AudioAssetForm,
    VideoAssetForm,
    )

# -------------------------------------- #
#         Facet Template Views           #
# -------------------------------------- #

# ACCESS: Only org users should be able to create a template for their org.
# Future, some thinking about how to handle this for shared facets...
class FacetTemplateCreateView(LoginRequiredMixin, CreateView):
    """Create a facet template."""

    model = FacetTemplate
    form_class = FacetTemplateForm

    template_name = 'editorial/facet/facettemplate_form.html'


    form_invalid_message = "Something went wrong."
    form_valid_message = "Template created."

    def form_valid(self, form):
        """Save -- but first adding owner and organization."""

        self.object = template = form.save(commit=False)

        form_fields = self.request.POST.getlist('fields')

        template.owner = self.request.user
        template.organization = self.request.user.organization
        template.fields_used = form_fields

        template.save()
        form.save_m2m()

        action.send(self.request.user, verb="created", action_object=self.object)

        return redirect(self.get_success_url())


# ACCESS: Only org users should be able to edit their org's templates.
class FacetTemplateUpdateView(LoginRequiredMixin, FormMessagesMixin, UpdateView):
    """Edit a facet template."""

    model = FacetTemplate
    form_class = FacetTemplateForm

    template_name = 'editorial/facet/facettemplate_form.html'

    form_invalid_message = "Something went wrong."
    form_valid_message = "Changes saved."

    def get_object(self):
        facettemplate = FacetTemplate.objects.get(pk=self.kwargs['template'])
        return facettemplate

    def form_valid(self, form):
        """Handle submission of form manually."""

        org = Organization.objects.get(pk=self.kwargs['org'])
        # Retrieve form values manually
        ft_id = self.request.POST.get('facettemplate')
        form_fields = self.request.POST.getlist('fields')
        name = self.request.POST.get('name')
        description = self.request.POST.get('description')
        is_active = form.cleaned_data['is_active']

        # Set new values
        facettemplate = FacetTemplate.objects.get(id=ft_id)
        facettemplate.name = name
        facettemplate.description = description
        facettemplate.is_active = is_active
        facettemplate.fields_used = form_fields
        facettemplate.save()

        action.send(self.request.user, verb="edited", action_object=self.object)

        return redirect('facet_template_list', org=org.id)


# ACCESS: Only org users should be able to see their org's templates.
class FacetTemplateListView(LoginRequiredMixin, FormMessagesMixin, TemplateView):
    """List all sitewide and organization facet templates. Distinguishes between
    active and not active templates.
    """

    context_object_name = 'facettemplates'
    template_name = 'editorial/facet/facettemplate_list.html'

    def get_context_data(self, **kwargs):
        """Group facettemplates for display."""

        context = super(FacetTemplateListView, self).get_context_data(**kwargs)
        org = Organization.objects.get(pk=self.kwargs['org'])
        basetemplates = FacetTemplate.objects.filter(organization_id__isnull=True)
        activetemplates = FacetTemplate.objects.filter(Q(organization_id=org) & Q(is_active=True))
        inactivetemplates = FacetTemplate.objects.filter(Q(organization_id=org) & Q(is_active=False))
        context['basetemplates'] = basetemplates
        context['activetemplates'] = activetemplates
        context['inactivetemplates'] = inactivetemplates
        return context


# ACCESS Only org users should be able to see detail pages for templates:
class FacetTemplateDetailView(LoginRequiredMixin, FormMessagesMixin, DetailView):
    """Used to display details about sitewide tempates that are not editable by users.

    For editable templates, the users are sent directly to the edit form for details.
    """

    model = FacetTemplate
    template_name = 'editorial/facet/facettemplate_detail.html'

    def get_object(self):
        return FacetTemplate.objects.get(pk=self.kwargs['template'])


# Access only org users should be able to delete templates that belong to their organization.
class FacetTemplateDeleteView(LoginRequiredMixin, FormMessagesMixin, DeleteView):
    """View for handling deletion of a facet template.

    In this project, we expect deletion to be done via a JS pop-up UI; we don't expect to
    actually use the "do you want to delete this?" Django-generated page. However, this is
    available if useful.
    """

    #FIXME troubleshoot delete js
    model = FacetTemplate
    template_name = "editorial/facet/facettemplate_delete.html"

    form_valid_message = "Deleted."
    form_invalid_message = "Please check form."

    def get_object(self):
        return FacetTemplate.objects.get(pk=self.kwargs['template'])

    def get_success_url(self):
        """Post-deletion, return to the template list."""

        return reverse('facet_template_list',kwargs={'org':self.request.user.organization.id})

# -------------------------------------- #
#           Facet Views                  #
# -------------------------------------- #

# ACCESS: Any org user, or user from an organization that is in collaborate_with
# should be able to create a facet for a story they have access to
# Contractors should only be able to do so for stories that they have access to
# That should be handled by limiting which story they have access to.
class FacetPreCreateView(FormMessagesMixin, FormView):
    """First step in creating a facet."""

    form_class = FacetPreCreateForm
    template_name = 'editorial/facet/facet_precreate_form.html'

    form_invalid_message = "Something went wrong."
    form_valid_message = "Facet started. Add a status, headline and content to get started."

    def get_form_kwargs(self):
        """Pass user organization to the form."""

        kw = super(FacetPreCreateView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def form_valid(self, form):
        """Redirect to real facet-creation form."""

        template = form.data['template']
        name = form.cleaned_data['name']

        url = reverse("facet_add",
                      kwargs={'template_id': template, 'story': self.kwargs['story']})
        return redirect("{}?name={}".format(url, name))


# ACCESS: Any org user, or user from an organization that is in collaborate_with
# should be able to create a facet for a story they have access to
# Contractors should only be able to do so for stories that they have access to
# That should be handled by limiting which story they have access to.
class FacetCreateView(LoginRequiredMixin, FormMessagesMixin, CreateView):
    """Create a facet (dynamically using right template)."""

    model = Facet
    template_name = 'editorial/facet/facet_form.html'

    form_invalid_message = "Something went wrong."
    form_valid_message = "Facet created."

    def get_form_class(self):
        """Get dynamic form, based on this template."""

        return get_facet_form_for_template(self.kwargs['template_id'])

    def get_form_kwargs(self):
        """Pass some initial things to scaffold form."""

        kwargs = super(FacetCreateView, self).get_form_kwargs()
        kwargs['template'] = FacetTemplate.objects.get(pk=self.kwargs['template_id'])
        kwargs['story'] = Story.objects.get(pk=self.kwargs['story'])
        kwargs['user'] = self.request.user
        kwargs['organization'] = self.request.user.organization
        return kwargs

    def get_initial(self):
        """Initial data for form:
        - name (optionally, from request data)
        """

        template = FacetTemplate.objects.get(pk=self.kwargs['template_id'])

        return {'name': self.request.GET.get('name', ''), 'template': template, 'content': 'Content here', 'status': 'Draft'}


# ACCESS: Any org user, or user from an organization that is in collaborate_with
# should be able to update a facet for a story they have access to
# Contractors should only be able to do so for stories that they have access to
# That should be handled by limiting which story they have access to.
class FacetUpdateView(LoginRequiredMixin, FormMessagesMixin, UpdateView):
    """Update a facet (dynamically using right template)."""

    model = Facet
    template_name = 'editorial/facet/facet_form.html'
    form_invalid_message = "Something went wrong."
    form_valid_message = "Changes saved."

    def get_form_class(self):
        """Get dynamic form based on this template."""

        return get_facet_form_for_template(self.object.template_id)

    def facet_discussion(self):
        """Get discussion, comments and comment form for the facet."""

        self.object = self.get_object()
        discussion = self.object.discussion
        comments = discussion.comment_set.all().order_by('date')
        form = CommentForm()
        return {'discussion': discussion, 'comments': comments, 'form': form}

    def facet_image_assets(self):
        """Return all image assets associated with a facet and the forms to associate more."""

        self.object = self.get_object()
        images = self.object.get_facet_images()
        org_images = self.object.organization.get_org_image_library()
        uploadform = ImageAssetForm()
        return {'images': images, 'org_images': org_images, 'uploadform': uploadform}

    def facet_document_assets(self):
        """Return all document assets associated with a facet and the forms to associate more."""

        self.object = self.get_object()
        documents = self.object.get_facet_documents()
        org_documents = self.object.organization.get_org_document_library()
        uploadform = DocumentAssetForm()
        return {'documents': documents, 'org_documents': org_documents, 'uploadform': uploadform}

    def facet_audio_assets(self):
        """Return all audio assets associated with a facet and the forms to associate more."""

        self.object = self.get_object()
        audio = self.object.get_facet_audio()
        org_audio = self.object.organization.get_org_audio_library()
        uploadform = AudioAssetForm()
        return {'audio': audio, 'org_audio': org_audio, 'uploadform': uploadform}

    def facet_video_assets(self):
        """Return all video assets associated with a facet and the forms to associate more."""

        self.object = self.get_object()
        videos = self.object.get_facet_video()
        org_videos = self.object.organization.get_org_video_library()
        uploadform = VideoAssetForm()
        return {'videos': videos, 'org_videos': org_videos, 'uploadform': uploadform}

    def facet_kwargs(self):
        """Return kwargs from url for navigation."""
        facet_kwargs = self.kwargs['pk']
        return facet_kwargs


# ACCESS: Only an org user that is an admin or editor should be able to delete a
# facet for one of their org's stories.
class FacetDeleteView(LoginRequiredMixin, FormMessagesMixin, DeleteView):
    """View for handling deletion of a facet.

    In this project, we expect deletion to be done via a JS pop-up UI; we don't expect to
    actually use the "do you want to delete this?" Django-generated page. However, this is
    available if useful.
    """

    model = Facet
    template_name = "editorial/facet/facet_delete.html"

    form_valid_message = "Deleted."
    form_invalid_message = "Please check form."

    def get_success_url(self):
        """Post-deletion, return to the story URL."""

        return Story.objects.get(pk=self.kwargs['story']).get_absolute_url()
