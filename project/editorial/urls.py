""" Forms for editorial app. """

from django.conf.urls import url, include

# from . import views
# from views import HomeView
from views import (
    generalviews,
    # assetviews,
    inboxviews,
    scheduleviews,
    organizationviews,
    userviews,
    networkviews,
    seriesviews,
    storyviews,
    assetviews,
    pushcontentviews,
    communicationviews,
    noteviews,
    downloadviews,
    scheduleviews)

from . import api

from views.searchviews import EditorialSearchView

urlpatterns = [
    #----------------------------------------------------------------------#
    #   Test URL - Used for non-destructive testing of templates/queries
    #----------------------------------------------------------------------#
    url(r'^test$', generalviews.test, name='test'),
    #----------------------------------------------------------------------#
    #   API URL - Used API endpoints
    #----------------------------------------------------------------------#
    url('^api/', include(api.router.urls)),
    #----------------------------------------------------------------------#
    #   WebFacet to WordPress URL - On demand pushing
    #----------------------------------------------------------------------#
    url(r'^webfacet/json/$', pushcontentviews.webfacet_json, name='webfacet_json'),
    # url(r'^webfacet/wordpress/$', pushcontentviews.push_webfacet_wp, name='push_webfacet_wp'),
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
    url(r'^schedulecontent$', scheduleviews.schedule_content, name='schedule-content'),
    #----------------------------------------------------------------------#
    #   Asset Library URLS
    #----------------------------------------------------------------------#
    url(r'^assets$', assetviews.asset_library, name='asset_library'),
    url(r'^asset/image/(?P<pk>[0-9]+)/$', assetviews.image_asset_detail, name='image_asset_detail'),
    url(r'^asset/document/(?P<pk>[0-9]+)/$', assetviews.document_asset_detail, name='document_asset_detail'),
    # url(r'^asset/(?P<pk>[0-9]+)/edit/$', assetviews.asset_edit, name='asset_edit'),
    #----------------------------------------------------------------------#
    #   Collaborations URLS
    #----------------------------------------------------------------------#
    url(r'^collaborations$', generalviews.collaborations, name='collaborations'),
    #----------------------------------------------------------------------#
    #   Team URLS
    #----------------------------------------------------------------------#
    url(r'^team$', generalviews.team_list, name='team_list'),
    #----------------------------------------------------------------------#
    #   Inbox URLS - Labeled as Inbox in navigation
    #----------------------------------------------------------------------#
    url(r'^inbox$', inboxviews.inbox, name='inbox'),
    url(r'^inbox/compose$', inboxviews.compose_message_html, name='compose_message_html'),
    url(r'^inbox/sent$', inboxviews.sent_html, name='sent_html'),
    url(r'^inbox/(?P<comment_type>[-\w]+)/comments$', inboxviews.comments_html, name='comments_html'),
    # url(r'^inbox/important$', inboxviews.inbox_important, name='inbox_important'),
    # url(r'^inbox/trash$', inboxviews.inbox_trash, name='inbox_trash'),
    #----------------------------------------------------------------------#
    #   Private Message URLS
    #----------------------------------------------------------------------#
    url(r'^privatemessage/new/$', communicationviews.private_message_new, name='private_message_new'),
    url(r'^privatemessage/(?P<pk>[0-9]+)/content/$', inboxviews.message_html, name='message_html'),
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
    url(r"^search/$", EditorialSearchView.as_view(), name="search"),
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
    url(r'^user/deactivate/$', userviews.user_deactivate, name='user_deactivate'),
    url(r'^user/activate/$', userviews.user_activate, name='user_activate'),
    #----------------------------------------------------------------------#
    #   Series URLS
    #----------------------------------------------------------------------#
    url(r'^series/new/$', seriesviews.series_new, name='series_new'),
    url(r'^series$', seriesviews.series_list, name='series_list'),
    url(r'^series/json$', seriesviews.series_json, name='series_json'),
    url(r'^series/(?P<pk>[0-9]+)/$', seriesviews.series_detail, name='series_detail'),
    url(r'^series/(?P<pk>[0-9]+)/edit/$', seriesviews.series_edit, name='series_edit'),
    url(r'^series/(?P<pk>[0-9]+)/delete/$', seriesviews.series_delete, name='series_delete'),
    url(r'^series/(?P<pk>[0-9]+)/notes/$', noteviews.series_notes, name='series_notes'),
    url(r'^series/note/new/$', noteviews.create_series_note, name='create_series_note'),
    #----------------------------------------------------------------------#
    #   Story URLS
    #----------------------------------------------------------------------#
    url(r'^story/new/$', storyviews.story_new, name='story_new'),
    url(r'^stories$', storyviews.story_list, name='story_list'),
    url(r'^story/(?P<pk>[0-9]+)/$', storyviews.story_detail, name='story_detail'),
    url(r'^story/(?P<pk>[0-9]+)/edit/$', storyviews.story_edit, name='story_edit'),
    url(r'^story/(?P<pk>[0-9]+)/delete/$', storyviews.story_delete, name='story_delete'),
    url(r'^story/note/new/$', noteviews.create_story_note, name='create_story_note'),
    url(r'^story/(?P<pk>[0-9]+)/team/json$', storyviews.story_team_options_json, name='story_team_options_json'),
    #----------------------------------------------------------------------#
    #   Update URLS
    #----------------------------------------------------------------------#
    # Story and Facet update urls will go here.
    #----------------------------------------------------------------------#
    #   Asset URLS
    #----------------------------------------------------------------------#
    # Images
    url(r'^webfacet/image/new/$', assetviews.upload_webfacet_image, name='upload_webfacet_image'),
    url(r'^printfacet/image/new/$', assetviews.upload_printfacet_image, name='upload_printfacet_image'),
    url(r'^audiofacet/image/new/$', assetviews.upload_audiofacet_image, name='upload_audiofacet_image'),
    url(r'^videofacet/image/new/$', assetviews.upload_videofacet_image, name='upload_videofacet_image'),
    url(r'^webfacet/image/add/$', assetviews.add_webfacet_image, name='add_webfacet_image'),
    url(r'^printfacet/image/add/$', assetviews.add_printfacet_image, name='add_printfacet_image'),
    url(r'^audiofacet/image/add/$', assetviews.add_audiofacet_image, name='add_audiofacet_image'),
    url(r'^videofacet/image/add/$', assetviews.add_videofacet_image, name='add_videofacet_image'),
    # Documents
    url(r'^webfacet/document/new/$', assetviews.upload_webfacet_document, name='upload_webfacet_document'),
    url(r'^printfacet/document/new/$', assetviews.upload_printfacet_document, name='upload_printfacet_document'),
    url(r'^audiofacet/document/new/$', assetviews.upload_audiofacet_document, name='upload_audiofacet_document'),
    url(r'^videofacet/document/new/$', assetviews.upload_videofacet_document, name='upload_videofacet_document'),
    url(r'^webfacet/document/add/$', assetviews.add_webfacet_document, name='add_webfacet_document'),
    url(r'^printfacet/document/add/$', assetviews.add_printfacet_document, name='add_printfacet_document'),
    url(r'^audiofacet/document/add/$', assetviews.add_audiofacet_document, name='add_audiofacet_document'),
    url(r'^videofacet/document/add/$', assetviews.add_videofacet_document, name='add_videofacet_document'),
    # Audio
    url(r'^webfacet/audio/new/$', assetviews.upload_webfacet_audio, name='upload_webfacet_audio'),
    url(r'^printfacet/audio/new/$', assetviews.upload_printfacet_audio, name='upload_printfacet_audio'),
    url(r'^audiofacet/audio/new/$', assetviews.upload_audiofacet_audio, name='upload_audiofacet_audio'),
    url(r'^videofacet/audio/new/$', assetviews.upload_videofacet_audio, name='upload_videofacet_audio'),
    url(r'^webfacet/audio/add/$', assetviews.add_webfacet_audio, name='add_webfacet_audio'),
    url(r'^printfacet/audio/add/$', assetviews.add_printfacet_audio, name='add_printfacet_audio'),
    url(r'^audiofacet/audio/add/$', assetviews.add_audiofacet_audio, name='add_audiofacet_audio'),
    url(r'^videofacet/audio/add/$', assetviews.add_videofacet_audio, name='add_videofacet_audio'),
    # Video
    url(r'^webfacet/video/new/$', assetviews.upload_webfacet_video, name='upload_webfacet_video'),
    # url(r'^printfacet/video/new/$', assetviews.upload_printfacet_video, name='upload_printfacet_video'),
    # url(r'^audiofacet/video/new/$', assetviews.upload_audiofacet_video, name='upload_audiofacet_video'),
    # url(r'^videofacet/video/new/$', assetviews.upload_videofacet_video, name='upload_videofacet_video'),
    url(r'^webfacet/video/add/$', assetviews.add_webfacet_video, name='add_webfacet_video'),
    # url(r'^printfacet/video/add/$', assetviews.add_printfacet_video, name='add_printfacet_video'),
    # url(r'^audiofacet/video/add/$', assetviews.add_audiofacet_video, name='add_audiofacet_video'),
    # url(r'^videofacet/video/add/$', assetviews.add_videofacet_video, name='add_videofacet_video'),
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
    # url(r'^network/stories/json$', networkviews.network_stories_json, name='network_stories_json'),
    url(r'^network/(?P<pk>[0-9]+)/notes/$', noteviews.network_notes, name='network_notes'),
    url(r'^network/note/new/$', noteviews.create_network_note, name='create_network_note'),
]
