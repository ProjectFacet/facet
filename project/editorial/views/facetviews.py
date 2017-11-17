from django.views.generic import CreateView, FormView, UpdateView
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from ..models import Facet
from ..forms import get_facet_form_for_template, FacetPreCreateForm




class FacetCreateView(CreateView):
    """Create a facet (dynamically using right template)."""

    model = Facet

    def get_form_class(self):
        """Get dynamic form based on this template."""

        return get_facet_form_for_template(self.kwargs['template_id'])

    def get_initial(self):
        """Initial data for form:

        - template-id (from URL)
        - name (optionally, from request data)
        """

        return {'template': self.kwargs['template_id'],
                'name': self.request.GET.get('name', '')}


class FacetPreCreateView(FormView):
    """First step in creating a facet."""

    form_class = FacetPreCreateForm
    template_name = "editorial/facet_precreate_form.html"

    def form_valid(self, form):
        """Redirect to real facet-creation form."""

        template = form.data['template']
        name = form.cleaned_data['name']

        url = reverse("facet_add", kwargs={'template_id': template})
        return redirect("{}?name={}".format(url, name))


class FacetUpdateView(UpdateView):
    """Update a facet (dynamically using right template)."""

    model = Facet

    def get_form_class(self):
        """Get dynamic form based on this template."""

        return get_facet_form_for_template(self.object.template_id)


class FacetDetailView(DetailView):
    """Display a facet and all it fields and assets."""

    model = Facet

    # def image_assets(self):
    #     # {% with imgs=images_assets %}
    #     #    {{ imgs.images }}
    #     #    {{ images.form }}
    #     # {% endwith %}
    #     image_library = self.request.user.organization.get_org_image_library()
    #     story_images = self.get_story_images()
    #     form = ImageAssetForm()
    #     return {'image_library': image_library, 'story_images': story_images, 'form': form}

    pass
