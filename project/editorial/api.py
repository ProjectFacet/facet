"""Editorial REST API.

REST API for facet content.

This API is to create posts in various CMS."""


from rest_framework import serializers, viewsets, routers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions

from .models import Facet, Organization, User

# -------------------------------------------------------------- #
# Facet Endpoint
# -------------------------------------------------------------- #

class FacetListSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for the main list of organization facets."""

    credit = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Facet
        fields = [
            'id',
            'title',
            'excerpt',
            'credit',
        ]


class FacetSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Facet content."""

    organization = serializers.PrimaryKeyRelatedField(read_only=True)
    credit = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    image_assets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    document_assets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    audio_assets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    video_assets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Facet
        fields = [
            'id',
            'headline',
            'excerpt',
            'content',
            'keywords',
            'organization',
            'credit',
            'image_assets',
            'document_assets',
            'audio_assets',
            'video_assets',
        ]


class FacetViewSet(viewsets.ReadOnlyModelViewSet):
    """Facets belonging to a specific organization."""

    queryset = (Facet.objects.all())

    serializer_class = FacetSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        """List of facets."""

        # organization = self.request.query_params.get('organization')
        organization = self.request.user.organization

        if organization:
            filters = {'organization': organization}
        else:
            filters = {}

        serializer = FacetListSerializer(
            self.get_queryset().filter(**filters),
            many=True,
            context={'request': self.request})

        return Response(
            serializer.data)


# -------------------------------------------------------------- #
# API Endpoint Routes
# -------------------------------------------------------------- #

router = routers.DefaultRouter()

router.register(r'facets', FacetViewSet)
