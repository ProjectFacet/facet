""" Forms for editorial app. """

from django.conf.urls import url, include

# from . import views
# from views import HomeView
from views import (
    generalviews,
    scheduleviews,
    organizationviews,
    userviews,
    networkviews,
    seriesviews,
    storyviews,
    assetviews,
    communicationviews,
    noteviews,
    downloadviews,
    scheduleviews)

from views.searchviews import EditorialSearchView

urlpatterns = [
    #----------------------------------------------------------------------#
    #   Test URL - Used for non-destructive testing of templates/queries
    #----------------------------------------------------------------------#
    url(r'^test$', generalviews.test, name='test'),
    #----------------------------------------------------------------------#
    #   Homepage URLS
    #----------------------------------------------------------------------#
    url(r'^$', generalviews.index, name='index'),
    # url(r'^$', HomeView.as_view(), name='index'),
    #----------------------------------------------------------------------#
    #   Dashboard URLS
    #----------------------------------------------------------------------#
    url(r'^dashboard$', generalviews.dashboard, name='dashboard'),
    #----------------------------------------------------------------------#
    #   Schedule URLS
    #----------------------------------------------------------------------#
    url(r'^schedule$', scheduleviews.schedule, name='schedule'),
    #----------------------------------------------------------------------#
    #   Collaborations URLS
    #----------------------------------------------------------------------#
    url(r'^collaborations$', generalviews.collaborations, name='collaborations'),
    #----------------------------------------------------------------------#
    #   Team URLS
    #----------------------------------------------------------------------#
    url(r'^team$', generalviews.team_list, name='team_list'),
    #----------------------------------------------------------------------#
    #   Discussion URLS
    #----------------------------------------------------------------------#
    # Labeled as Inbox in navigation
    url(r'^discussion$', generalviews.discussion, name='discussion'),
    #----------------------------------------------------------------------#
    #   Private Message URLS
    #----------------------------------------------------------------------#
    url(r'^privatemessage/new/$', communicationviews.private_message_new, name='private_message_new'),
    #----------------------------------------------------------------------#
    #   Comment URLS
    #----------------------------------------------------------------------#
    url(r'^organizationcomment/new$', communicationviews.create_orgcomment, name='create_orgcomment'),
    url(r'^organization/comments$', communicationviews.org_comments, name='org_comments'),
    url(r'^networkcomment/new$', communicationviews.create_networkcomment, name='create_networkcomment'),
    url(r'^seriescomment/new$', communicationviews.create_seriescomment, name='create_seriescomment'),
    url(r'^storycomment/new$', communicationviews.create_storycomment, name='create_storycomment'),
    url(r'^webcomment/new$', communicationviews.create_webcomment, name='create_webcomment'),
    url(r'^printcomment/new$', communicationviews.create_printcomment, name='create_printcomment'),
    url(r'^audiocomment/new$', communicationviews.create_audiocomment, name='create_audiocomment'),
    url(r'^videocomment/new$', communicationviews.create_videocomment, name='create_videocomment'),
    #----------------------------------------------------------------------#
    #   Organization URLS
    #----------------------------------------------------------------------#
    url(r'^organization/new$', organizationviews.org_new, name="org_new"),
    url(r'^organization/(?P<pk>[0-9]+)/$', organizationviews.org_detail, name='org_detail'),
    url(r'^organization/(?P<pk>[0-9]+)/edit/$', organizationviews.org_edit, name='org_edit'),
    url(r'^organization/(?P<pk>[0-9]+)/notes/$', noteviews.org_notes, name='org_notes'),
    url(r'^organization/note/new/$', noteviews.create_org_note, name='create_org_note'),
    #----------------------------------------------------------------------#
    #   User URLS
    #----------------------------------------------------------------------#
    url(r'^user/new/$', userviews.user_new, name='user_new'),
    url(r'^user/(?P<pk>[0-9]+)/$', userviews.user_detail, name='user_detail'),
    url(r'^user/(?P<pk>[0-9]+)/edit/$', userviews.user_edit, name='user_edit'),
    url(r'^user/(?P<pk>[0-9]+)/notes/$', noteviews.user_notes, name='user_notes'),
    url(r'^user/note/new/$', noteviews.create_user_note, name='create_user_note'),
    #----------------------------------------------------------------------#
    #   Series URLS
    #----------------------------------------------------------------------#
    url(r'^series/new/$', seriesviews.series_new, name='series_new'),
    url(r'^series$', seriesviews.series_list, name='series_list'),
    url(r'^series/(?P<pk>[0-9]+)/$', seriesviews.series_detail, name='series_detail'),
    url(r'^series/(?P<pk>[0-9]+)/edit/$', seriesviews.series_edit, name='series_edit'),
    url(r'^series/(?P<pk>[0-9]+)/notes/$', noteviews.series_notes, name='series_notes'),
    url(r'^series/note/new/$', noteviews.create_series_note, name='create_series_note'),
    #----------------------------------------------------------------------#
    #   Story URLS
    #----------------------------------------------------------------------#
    url(r'^story/new/$', storyviews.story_new, name='story_new'),
    url(r'^stories$', storyviews.story_list, name='story_list'),
    url(r'^story/(?P<pk>[0-9]+)/$', storyviews.story_detail, name='story_detail'),
    url(r'^story/(?P<pk>[0-9]+)/edit/$', storyviews.story_edit, name='story_edit'),
    url(r'^story/note/new/$', noteviews.create_story_note, name='create_story_note'),
    #----------------------------------------------------------------------#
    #   Asset URLS
    #----------------------------------------------------------------------#
    url(r'^webfacet/image/new/$', assetviews.upload_webfacet_image, name='upload_webfacet_image'),
    url(r'^printfacet/image/new/$', assetviews.upload_printfacet_image, name='upload_printfacet_image'),
    url(r'^audiofacet/image/new/$', assetviews.upload_audiofacet_image, name='upload_audiofacet_image'),
    url(r'^videofacet/image/new/$', assetviews.upload_videofacet_image, name='upload_videofacet_image'),
    url(r'^webfacet/image/add/$', assetviews.add_webfacet_image, name='add_webfacet_image'),
    url(r'^printfacet/image/add/$', assetviews.add_printfacet_image, name='add_printfacet_image'),
    url(r'^audiofacet/image/add/$', assetviews.add_audiofacet_image, name='add_audiofacet_image'),
    url(r'^videofacet/image/add/$', assetviews.add_videofacet_image, name='add_videofacet_image'),
    #----------------------------------------------------------------------#
    #   Network URLS
    #----------------------------------------------------------------------#
    url(r'^network/new/$', networkviews.network_new, name='network_new'),
    url(r'^network/(?P<pk>[0-9]+)/$', networkviews.network_detail, name='network_detail'),
    url(r'^network/invitation/$', networkviews.send_network_invite, name='send_network_invite'),
    url(r'^network/invitation/accept/$', networkviews.confirm_network_invite, name='confirm_network_invite'),
    url(r'^network/(?P<pk>[0-9]+)/edit/$', networkviews.network_edit, name='network_edit'),
    url(r'^network/list$', networkviews.network_list, name='network_list'),
    url(r'^network/stories$', networkviews.network_stories, name='network_stories'),
    url(r'^network/(?P<pk>[0-9]+)/notes/$', noteviews.network_notes, name='network_notes'),
    url(r'^network/note/new/$', noteviews.create_network_note, name='create_network_note'),
    #----------------------------------------------------------------------#
    #   Copy URLS
    #----------------------------------------------------------------------#
    url(r'^story/copy/(?P<pk>[0-9]+)/$', networkviews.copy_network_story, name='copy_network_story'),
    #----------------------------------------------------------------------#
    #   Download URLS
    #----------------------------------------------------------------------#
    url(r'^story/(?P<pk>[0-9]+)/download/$', downloadviews.create_download, name='create_download'),
    #----------------------------------------------------------------------#
    #   Search URLS
    #----------------------------------------------------------------------#
    url(r"^search/", include("watson.urls", namespace="watson")),
    # url(r"^search/", EditorialSearchView.as_view()),
]
