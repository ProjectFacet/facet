""" Model for editorial application.

    Models
    ======
    People: User, Organization, Network
    Contributors: ContributorInfo, OrganizationContributorInfo
    Platforms: Platform, PlatformAccount
    Projects: Project
    Series: Series
    Story: Story
    Facet: FacetTemplate, Facet, FacetContributor, ContentLicense
           - (Temp: Versions of above for web, print, audio, video facets)
    Copy: SeriesCopyDetail, StoryCopyDetail, FacetCopyDetail, ImageAssetCopyDetail,
          DocumentAssetCopyDetail, AudioAssetCopyDetail, VideoAssetCopyDetail
          - (Temp: Versions of above for web, print, audio, video facets)
    Tasks: Task
    Events: Event
    Assets: BaseAsset, BaseAssetMetadata,
            BaseImage, ImageAsset, SimpleImage,
            BaseDocument, DocumentAsset, DocumentImage,
            BaseAudio, AudioAsset, SimpleAudio,
            BaseVideo, VideoAsset, SimpleVideo,
    Notes: (Base)Note, NetworkNote, OrganizationNote, UserNote, ProjectNote, SeriesNote, StoryNote
    Discussion: Discussion, PrivateDiscussion, PrivateMessage, Comment, CommentReadStatus

"""

from .people import User, Organization, Network, OrganizationSubscription
from .assets import ImageAsset, DocumentAsset, AudioAsset, VideoAsset
from .assets import SimpleImage, SimpleDocument, SimpleAudio, SimpleVideo
from .discussion import Discussion, Comment, PrivateMessage
from .projects import Project
from .series import Series
from .story import Story
from .facets import Facet, FacetTemplate, ContentLicense
from .notes import Note
from .platforms import Platform, PlatformAccount
from .tasks import Task
from .events import Event
from .copy import *   # XXX
from .contractors import ContractorProfile, TalentEditorProfile, ContractorSubscription, OrganizationContractorAffiliation, Pitch, Call, Assignment
from .platforms import Platform, PlatformAccount


#-----------------------------------------------------------------------#
#  SOCIAL POST
#-----------------------------------------------------------------------#

# XXX Leaving this commented out for now to think about how to best
# relate or make use of Platform and PlatformAccount in the options.

# class SocialPost(models.Model):
#     """A social post.
#
#     A social post to promote a project, series, story or event.
#     """
#
#     FACEBOOK = 'Facebook'
#     TWITTER = 'Twitter'
#     INSTAGRAM = 'Instagram'
#     SOCIAL_ACCOUNT_CHOICES = (
#         (FACEBOOK, 'Facebook'),
#         (TWITTER, 'Twitter'),
#         (INSTAGRAM, 'Instagram'),
#     )
#
#     social_platform = models.CharField(
#         max_length=50,
#         choices=SOCIAL_ACCOUNT_CHOICES,
#         help_text='Platform the post is created for.'
#     )
#
#     text = models.TextField(
#         help_text='Content of the post.'
#     )
#
#     # a social post can be associated with a project, series, story or an event.
#     # Add connection to P, Se, St, or E
#
#     # Add Image assets for social posts to Assets section.
#
