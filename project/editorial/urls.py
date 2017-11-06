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
    projectviews,
    seriesviews,
    storyviews,
    taskviews,
    eventviews,
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
    url(r'^asset/audio/(?P<pk>[0-9]+)/$', assetviews.audio_asset_detail, name='audio_asset_detail'),
    url(r'^asset/video/(?P<pk>[0-9]+)/$', assetviews.video_asset_detail, name='video_asset_detail'),
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
    url(r'^projectcomment/new$', communicationviews.create_projectcomment, name='create_projectcomment'),
    url(r'^seriescomment/new$', communicationviews.create_seriescomment, name='create_seriescomment'),
    url(r'^storycomment/new$', communicationviews.create_storycomment, name='create_storycomment'),
    url(r'^webcomment/new$', communicationviews.create_webcomment, name='create_webcomment'),
    url(r'^printcomment/new$', communicationviews.create_printcomment, name='create_printcomment'),
    url(r'^audiocomment/new$', communicationviews.create_audiocomment, name='create_audiocomment'),
    url(r'^videocomment/new$', communicationviews.create_videocomment, name='create_videocomment'),
    #----------------------------------------------------------------------#
    #   Organization URLS
    #----------------------------------------------------------------------#
    url(r'^organization/new$', organizationviews.OrganizationCreateView.as_view(), name="org_new"),
    url(r'^organization/(?P<pk>[0-9]+)/$', organizationviews.OrganizationDetailView.as_view(), name='org_detail'),
    url(r'^organization/(?P<pk>[0-9]+)/edit/$', organizationviews.OrganizationUpdateView.as_view(), name='org_edit'),
    url(r'^organization/(?P<pk>[0-9]+)/notes/$', noteviews.org_notes, name='org_notes'),
    url(r'^organization/(?P<pk>[0-9]+)/note/(?P<note_type>[-\w]+)/content$', noteviews.note_content_html, name='note_content_html'),
    url(r'^organization/note/new/$', noteviews.create_org_note, name='create_org_note'),
    #----------------------------------------------------------------------#
    #   User URLS
    #----------------------------------------------------------------------#
    url(r'^user/new/$', userviews.user_new, name='user_new'),
    url(r'^user/(?P<pk>[0-9]+)/$', userviews.user_detail, name='user_detail'),
    url(r'^user/(?P<pk>[0-9]+)/edit/$', userviews.user_edit, name='user_edit'),
    url(r'^user/(?P<pk>[0-9]+)/notes/$', noteviews.user_notes, name='user_notes'),
    url(r'^user/(?P<pk>[0-9]+)/note/(?P<note_type>[-\w]+)/content$', noteviews.note_content_html, name='note_content_html'),
    url(r'^user/note/new/$', noteviews.create_user_note, name='create_user_note'),
    url(r'^user/deactivate/$', userviews.user_deactivate, name='user_deactivate'),
    url(r'^user/activate/$', userviews.user_activate, name='user_activate'),
    #----------------------------------------------------------------------#
    #   Project URLS
    #----------------------------------------------------------------------#
    url(r'^project/new/$', projectviews.project_new, name='project_new'),
    url(r'^projects$', projectviews.project_list, name='project_list'),
    url(r'^project/(?P<pk>[0-9]+)/$', projectviews.project_detail, name='project_detail'),
    url(r'^project/(?P<pk>[0-9]+)/edit/$', projectviews.project_edit, name='project_edit'),
    url(r'^project/(?P<pk>[0-9]+)/delete/$', projectviews.project_delete, name='project_delete'),
    url(r'^project/(?P<pk>[0-9]+)/notes/$', noteviews.project_notes, name='project_notes'),
    url(r'^project/(?P<pk>[0-9]+)/note/(?P<note_type>[-\w]+)/content$', noteviews.note_content_html, name='note_content_html'),
    url(r'^project/note/new/$', noteviews.create_project_note, name='create_project_note'),
    url(r'^project/(?P<pk>[0-9]+)/schedule/$', projectviews.project_schedule, name='project_schedule'),
    url(r'^project/(?P<pk>[0-9]+)/assets/$', projectviews.project_assets, name='project_assets'),
    url(r'^project/(?P<pk>[0-9]+)/stories/$', projectviews.project_stories, name='project_stories'),
    url(r'^project/(?P<pk>[0-9]+)/events/$', projectviews.project_events, name='project_events'),
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
    url(r'^series/(?P<pk>[0-9]+)/note/(?P<note_type>[-\w]+)/content$', noteviews.note_content_html, name='note_content_html'),
    url(r'^series/note/new/$', noteviews.create_series_note, name='create_series_note'),
    #----------------------------------------------------------------------#
    #   Story URLS
    #----------------------------------------------------------------------#
    url(r'^story/new/$', storyviews.story_new, name='story_new'),
    url(r'^stories$', storyviews.story_list, name='story_list'),
    url(r'^story/(?P<pk>[0-9]+)/$', storyviews.story_detail, name='story_detail'),
    url(r'^story/(?P<pk>[0-9]+)/edit/$', storyviews.story_edit, name='story_edit'),
    url(r'^story/(?P<pk>[0-9]+)/delete/$', storyviews.story_delete, name='story_delete'),
    url(r'^story/(?P<pk>[0-9]+)/notes/$', noteviews.story_notes, name='story_notes'),
    url(r'^story/(?P<pk>[0-9]+)/note/(?P<note_type>[-\w]+)/content$', noteviews.note_content_html, name='note_content_html'),
    url(r'^story/note/new/$', noteviews.create_story_note, name='create_story_note'),
    url(r'^story/(?P<pk>[0-9]+)/team/json$', storyviews.story_team_options_json, name='story_team_options_json'),
    #----------------------------------------------------------------------#
    #   Task URLS
    #----------------------------------------------------------------------#
    url(r'^task/new/$', taskviews.task_new, name='task_new'),
    url(r'^task/(?P<pk>[0-9]+)/$', taskviews.task_detail, name='task_detail'),
    url(r'^project/(?P<pk>[0-9]+)/tasks/$', taskviews.project_task_list, name='project_task_list'),
    url(r'^series/(?P<pk>[0-9]+)/tasks/$', taskviews.series_task_list, name='series_task_list'),
    url(r'^story/(?P<pk>[0-9]+)/tasks/$', taskviews.story_task_list, name='story_task_list'),
    url(r'^event/(?P<pk>[0-9]+)/tasks/$', taskviews.event_task_list, name='event_task_list'),
    #----------------------------------------------------------------------#
    #   Event URLS
    #----------------------------------------------------------------------#
    url(r'^event/new/$', eventviews.event_new, name='event_new'),
    url(r'^event/(?P<pk>[0-9]+)/$', eventviews.event_detail, name='event_detail'),

    #----------------------------------------------------------------------#
    #   Update URLS
    #----------------------------------------------------------------------#
    # Story and Facet update urls will go here.
    #----------------------------------------------------------------------#
    #   Asset URLS
    #----------------------------------------------------------------------#
    # Images
    url(r'^image/new/$', assetviews.upload_image, name='upload_image'),
    url(r'^image/add/$', assetviews.add_image, name='add_image'),
    # Documents
    url(r'^document/new/$', assetviews.upload_document, name='upload_document'),
    url(r'^document/add/$', assetviews.add_document, name='add_document'),
    # Audio
    url(r'^audio/new/$', assetviews.upload_audio, name='upload_audio'),
    url(r'^audio/add/$', assetviews.add_audio, name='add_audio'),
    # Video
    url(r'^video/new/$', assetviews.upload_video, name='upload_video'),
    url(r'^video/add/$', assetviews.add_video, name='add_video'),
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
    url(r'^network/(?P<pk>[0-9]+)/note/(?P<note_type>[-\w]+)/content$', noteviews.note_content_html, name='note_content_html'),
    url(r'^network/note/new/$', noteviews.create_network_note, name='create_network_note'),
]
