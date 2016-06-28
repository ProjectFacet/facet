"""Editorial REST API.

REST API for webfacet content.

This API is to create posts in various CMS."""


from rest_framework import serializers, viewsets, routers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions

from .models import WebFacet, Organization, User

# -------------------------------------------------------------- #
# WebFacet Endpoint
# -------------------------------------------------------------- #

class WebFacetListSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for the main list of organization webfacets."""

    credit = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = WebFacet
        fields = [
            'id',
            'title',
            'excerpt',
            'credit',
        ]


class WebFacetSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for WebFacet content."""

    organization = serializers.PrimaryKeyRelatedField(read_only=True)
    credit = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    image_assets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    document_assets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    audio_assets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    video_assets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = WebFacet
        fields = [
            'id',
            'title',
            'excerpt',
            'wf_content',
            'keywords',
            'organization',
            'credit',
            'image_assets',
            'document_assets',
            'audio_assets',
            'video_assets',
        ]


class WebFacetViewSet(viewsets.ReadOnlyModelViewSet):
    """WebFacets belonging to a specific organization."""

    queryset = (WebFacet.objects.all())

    serializer_class = WebFacetSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        """List of webfacets."""

        # organization = self.request.query_params.get('organization')
        organization = self.request.user.organization

        if organization:
            filters = {'organization': organization}
        else:
            filters = {}

        serializer = WebFacetListSerializer(
            self.get_queryset().filter(**filters),
            many=True,
            context={'request': self.request})

        return Response(
            serializer.data)


# -------------------------------------------------------------- #
# API Endpoint Routes
# -------------------------------------------------------------- #

router = routers.DefaultRouter()

router.register(r'webfacets', WebFacetViewSet)
