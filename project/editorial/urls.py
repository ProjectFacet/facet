""" Forms for editorial app. """

from django.conf.urls import url, include

# from . import views
# from views import HomeView
from views import (
    generalviews,
    accountviews,
    assetviews,
    inboxviews,
    scheduleviews,
    organizationviews,
    userviews,
    contractorviews,
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
    scheduleviews,
    facetviews,
    platformviews,
    )

from . import api

from views.searchviews import EditorialSearchView

urlpatterns = [
    #----------------------------------------------------------------------#
    #   Account URLS
    #----------------------------------------------------------------------#
    url(r'^account/selection/$', accountviews.AccountSelectionView.as_view(), name='account_selection'),
    #----------------------------------------------------------------------#
    #   Test URL - Used for non-destructive testing of templates/queries
    #----------------------------------------------------------------------#
    url(r'^test$', generalviews.TestTemplateView.as_view(), name='test'),
    #----------------------------------------------------------------------#
    #   API URL - Used API endpoints
    #----------------------------------------------------------------------#
    url('^api/', include(api.router.urls)),
    #----------------------------------------------------------------------#
    #   Facet to WordPress URL - On demand pushing
    #----------------------------------------------------------------------#
    url(r'^facet/json/$', pushcontentviews.webfacet_json, name='webfacet_json'),
    # url(r'^webfacet/wordpress/$', pushcontentviews.push_webfacet_wp, name='push_webfacet_wp'),
    #----------------------------------------------------------------------#
    #   Homepage URLS
    #----------------------------------------------------------------------#
    url(r'^$', generalviews.LandingTemplateView.as_view(), name='index'),
    # url(r'^$', HomeView.as_view(), name='index'),
    #----------------------------------------------------------------------#
    #   Dashboard URLS
    #----------------------------------------------------------------------#
    url(r'^dashboard$', generalviews.TeamUserDashboardTemplateView.as_view(), name='dashboard'),
    #----------------------------------------------------------------------#
    #   Schedule URLS
    #----------------------------------------------------------------------#
    url(r'^schedule$', scheduleviews.schedule, name='schedule'),
    url(r'^schedulecontent$', scheduleviews.schedule_content, name='schedule-content'),
    #----------------------------------------------------------------------#
    #   Asset Library URLS
    #----------------------------------------------------------------------#
    url(r'^assets$', assetviews.AssetLibraryTemplateView.as_view(), name='asset_library'),
    url(r'^asset/image/(?P<pk>[0-9]+)/$', assetviews.ImageAssetUpdateView.as_view(), name='image_asset_detail'),
    url(r'^asset/document/(?P<pk>[0-9]+)/$', assetviews.DocumentAssetUpdateView.as_view(), name='document_asset_detail'),
    url(r'^asset/audio/(?P<pk>[0-9]+)/$', assetviews.AudioAssetUpdateView.as_view(), name='audio_asset_detail'),
    url(r'^asset/video/(?P<pk>[0-9]+)/$', assetviews.VideoAssetUpdateView.as_view(), name='video_asset_detail'),
    # url(r'^asset/(?P<pk>[0-9]+)/edit/$', assetviews.asset_edit, name='asset_edit'),
    #----------------------------------------------------------------------#
    #   Collaborations URLS
    #----------------------------------------------------------------------#
    url(r'^collaborations$', generalviews.CollaborationTemplateView.as_view(), name='collaborations'),
    #----------------------------------------------------------------------#
    #   Team URLS
    #----------------------------------------------------------------------#
    url(r'^team$', generalviews.TeamTemplateView.as_view(), name='team_list'),
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
    url(r'^facetcomment/new$', communicationviews.create_facetcomment, name='create_facetcomment'),
    #----------------------------------------------------------------------#
    #   Platform URLS
    #----------------------------------------------------------------------#
    url(r'^user/(?P<pk>[0-9]+)/platformaccounts/edit/$', platformviews.UserPlatformAccountCreateView.as_view(), name='user_platformaccounts_create'),
    # url(r'^organization/(?P<pk>[0-9]+)/platformaccounts/edit/$', platformviews.organization_platformaccounts_create, name='organization_platformaccounts_create'),
    # url(r'^project/(?P<pk>[0-9]+)/platformaccounts/edit/$', platformviews.project_platformaccounts_create, name='project_platformaccounts_create'),
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
    url(r'^user/new/$', userviews.UserCreateView.as_view(), name='user_new'),
    url(r'^user/(?P<pk>[0-9]+)/$', userviews.UserDetailView.as_view(), name='user_detail'),
    url(r'^user/(?P<pk>[0-9]+)/edit/$', userviews.UserUpdateView.as_view(), name='user_edit'),
    url(r'^user/(?P<pk>[0-9]+)/notes/$', noteviews.user_notes, name='user_notes'),
    url(r'^user/(?P<pk>[0-9]+)/note/(?P<note_type>[-\w]+)/content$', noteviews.note_content_html, name='note_content_html'),
    url(r'^user/note/new/$', noteviews.create_user_note, name='create_user_note'),
    url(r'^user/deactivate/$', userviews.user_deactivate, name='user_deactivate'),
    url(r'^user/activate/$', userviews.user_activate, name='user_activate'),
    #----------------------------------------------------------------------#
    #   Contractor URLS
    #----------------------------------------------------------------------#
    url(r'^contractor/new/$', contractorviews.ContractorCreateView.as_view(), name='contractor_new'),
    url(r'^contractor/(?P<pk>[0-9]+)/$', contractorviews.ContractorDetailView.as_view(), name='contractor_detail'),
    url(r'^contractor/(?P<pk>[0-9]+)/edit/$', contractorviews.ContractorUpdateView.as_view(), name='contractor_edit'),
    url(r'^contractor/list/$', contractorviews.PublicContractorListView.as_view(), name='public_contractor_list'),
    url(r'^editor/list/$', contractorviews.PublicEditorListView.as_view(), name='public_editor_list'),
    url(r'^assignment/new/$', contractorviews.AssignmentCreateView.as_view(), name='assignment_new'),
    url(r'^assignment/(?P<pk>[0-9]+)/$', contractorviews.AssignmentDetailView.as_view(), name='assignment_detail'),
    url(r'^assignment/(?P<pk>[0-9]+)/edit/$', contractorviews.AssignmentUpdateView.as_view(), name='assignment_edit'),
    url(r'^call/new/$', contractorviews.CallCreateView.as_view(), name='call_new'),
    url(r'^call/(?P<pk>[0-9]+)/$', contractorviews.CallDetailView.as_view(), name='call_detail'),
    url(r'^call/(?P<pk>[0-9]+)/edit/$', contractorviews.CallUpdateView.as_view(), name='call_edit'),
    url(r'^pitch/new/$', contractorviews.PitchCreateView.as_view(), name='pitch_new'),
    url(r'^pitch/(?P<pk>[0-9]+)/$', contractorviews.PitchDetailView.as_view(), name='pitch_detail'),
    url(r'^pitch/(?P<pk>[0-9]+)/edit/$', contractorviews.PitchUpdateView.as_view(), name='pitch_edit'),
    #----------------------------------------------------------------------#
    #   Project URLS
    #----------------------------------------------------------------------#
    url(r'^project/new/$', projectviews.ProjectCreateView.as_view(), name='project_new'),
    url(r'^projects$', projectviews.ProjectListView.as_view(), name='project_list'),
    url(r'^project/(?P<pk>[0-9]+)/$', projectviews.ProjectDetailView.as_view(), name='project_detail'),
    url(r'^project/(?P<pk>[0-9]+)/edit/$', projectviews.ProjectUpdateView.as_view(), name='project_edit'),
    url(r'^project/(?P<pk>[0-9]+)/delete/$', projectviews.project_delete, name='project_delete'),
    url(r'^project/(?P<pk>[0-9]+)/notes/$', noteviews.project_notes, name='project_notes'),
    url(r'^project/(?P<pk>[0-9]+)/note/(?P<note_type>[-\w]+)/content$', noteviews.note_content_html, name='note_content_html'),
    url(r'^project/note/new/$', noteviews.create_project_note, name='create_project_note'),
    url(r'^project/(?P<pk>[0-9]+)/schedule/$', projectviews.project_schedule, name='project_schedule'),
    url(r'^project/(?P<pk>[0-9]+)/assets/$', projectviews.ProjectAssetTemplateView.as_view(), name='project_assets'),
    url(r'^project/(?P<pk>[0-9]+)/stories/$', projectviews.ProjectStoryTemplateView.as_view(), name='project_stories'),
    #----------------------------------------------------------------------#
    #   Series URLS
    #----------------------------------------------------------------------#
    url(r'^series/new/$', seriesviews.SeriesCreateView.as_view(), name='series_new'),
    url(r'^series$', seriesviews.SeriesListView.as_view(), name='series_list'),
    url(r'^series/json$', seriesviews.series_json, name='series_json'),
    url(r'^series/(?P<pk>[0-9]+)/$', seriesviews.SeriesDetailView.as_view(), name='series_detail'),
    url(r'^series/(?P<pk>[0-9]+)/edit/$', seriesviews.SeriesUpdateView.as_view(), name='series_edit'),
    url(r'^series/(?P<pk>[0-9]+)/delete/$', seriesviews.series_delete, name='series_delete'),
    url(r'^series/(?P<pk>[0-9]+)/notes/$', noteviews.series_notes, name='series_notes'),
    url(r'^series/(?P<pk>[0-9]+)/note/(?P<note_type>[-\w]+)/content$', noteviews.note_content_html, name='note_content_html'),
    url(r'^series/note/new/$', noteviews.create_series_note, name='create_series_note'),
    #----------------------------------------------------------------------#
    #   Story URLS
    #----------------------------------------------------------------------#
    url(r'^story/new/$', storyviews.StoryCreateView.as_view(), name='story_new'),
    url(r'^stories$', storyviews.StoryListView.as_view(), name='story_list'),
    url(r'^story/(?P<pk>[0-9]+)/$', storyviews.StoryDetailView.as_view(), name='story_detail'),
    url(r'^story/(?P<pk>[0-9]+)/edit/$', storyviews.StoryUpdateView.as_view(), name='story_edit'),
    url(r'^story/(?P<pk>[0-9]+)/delete/$', storyviews.StoryDeleteView.as_view(), name='story_delete'),
    url(r'^story/(?P<pk>[0-9]+)/schedule/$', storyviews.story_schedule, name='story_schedule'),
    url(r'^story/(?P<pk>[0-9]+)/notes/$', noteviews.story_notes, name='story_notes'),
    url(r'^story/(?P<pk>[0-9]+)/note/(?P<note_type>[-\w]+)/content$', noteviews.note_content_html, name='note_content_html'),
    url(r'^story/note/new/$', noteviews.create_story_note, name='create_story_note'),
    url(r'^story/(?P<pk>[0-9]+)/team/json$', storyviews.story_team_options_json, name='story_team_options_json'),
    #----------------------------------------------------------------------#
    #   Facet URLS
    #----------------------------------------------------------------------#
    url(r'^facet/add/$', facetviews.FacetPreCreateView.as_view(), name="facet_precreate"),
    url(r'^facet/add/(?P<template_id>\d+)/$', facetviews.FacetCreateView.as_view(), name="facet_add"),
    url(r'^facet/edit/(?P<pk>\d+)/$', facetviews.FacetUpdateView.as_view(), name="facet_edit"),
    url(r'^facet/template/create/$', facetviews.FacetTemplateCreateView.as_view(), name="facet_template_create"),
    url(r'^facet/template/(?P<pk>\d+)/edit$', facetviews.FacetTemplateUpdateView.as_view(), name="facet_template_edit"),
    #----------------------------------------------------------------------#
    #   Task URLS
    #----------------------------------------------------------------------#
    url(r'^task/new/$', taskviews.TaskCreateView.as_view(), name='task_new'),
    url(r'^task/(?P<pk>[0-9]+)/$', taskviews.TaskUpdateView.as_view(), name='task_detail'),
    url(r'^project/(?P<pk>[0-9]+)/tasks/$', taskviews.ProjectTaskTemplateView.as_view(), name='project_task_list'),
    url(r'^series/(?P<pk>[0-9]+)/tasks/$', taskviews.SeriesTaskTemplateView.as_view(), name='series_task_list'),
    url(r'^story/(?P<pk>[0-9]+)/tasks/$', taskviews.StoryTaskTemplateView.as_view(), name='story_task_list'),
    url(r'^event/(?P<pk>[0-9]+)/tasks/$', taskviews.EventTaskTemplateView.as_view(), name='event_task_list'),
    #----------------------------------------------------------------------#
    #   Event URLS
    #----------------------------------------------------------------------#
    url(r'^event/new/$', eventviews.EventCreateView.as_view(), name='event_new'),
    url(r'^event/(?P<pk>[0-9]+)/$', eventviews.EventUpdateView.as_view(), name='event_detail'),
    url(r'^organization/(?P<pk>[0-9]+)/events/$', eventviews.OrganizationEventTemplateView.as_view(), name='organization_event_list'),
    url(r'^project/(?P<pk>[0-9]+)/events/$', eventviews.ProjectEventTemplateView.as_view(), name='project_event_list'),
    url(r'^series/(?P<pk>[0-9]+)/events/$', eventviews.SeriesEventTemplateView.as_view(), name='series_event_list'),
    url(r'^story/(?P<pk>[0-9]+)/events/$', eventviews.StoryEventTemplateView.as_view(), name='story_event_list'),
    #----------------------------------------------------------------------#
    #   Asset URLS
    #----------------------------------------------------------------------#
    # Images
    url(r'^image/new/$', assetviews.ImageAssetCreateView.as_view(), name='upload_image'),
    url(r'^image/add/$', assetviews.add_image, name='add_image'),
    # Documents
    url(r'^document/new/$', assetviews.DocumentAssetCreateView.as_view(), name='upload_document'),
    url(r'^document/add/$', assetviews.add_document, name='add_document'),
    # Audio
    url(r'^audio/new/$', assetviews.AudioAssetCreateView.as_view(), name='upload_audio'),
    url(r'^audio/add/$', assetviews.add_audio, name='add_audio'),
    # Video
    url(r'^video/new/$', assetviews.VideoAssetCreateView.as_view(), name='upload_video'),
    url(r'^video/add/$', assetviews.add_video, name='add_video'),
    # Simple Images
    url(r'^simpleimage/new/$', assetviews.SimpleImageCreateView.as_view(), name='upload_simple_image'),
    # Simple documents
    url(r'^simpledocument/new/$', assetviews.SimpleDocumentCreateView.as_view(), name='upload_simple_document'),
    # Simple Audio
    url(r'^simpleaudio/new/$', assetviews.SimpleAudioCreateView.as_view(), name='upload_simple_audio'),
    # Simple Video
    url(r'^simplevideo/new/$', assetviews.SimpleVideoCreateView.as_view(), name='upload_simple_video'),
    #----------------------------------------------------------------------#
    #   Network URLS
    #----------------------------------------------------------------------#
    url(r'^network/new/$', networkviews.NetworkCreateView.as_view(), name='network_new'),
    url(r'^network/(?P<pk>[0-9]+)/$', networkviews.NetworkDetailView.as_view(), name='network_detail'),
    url(r'^network/invitation/$', networkviews.send_network_invite, name='send_network_invite'),
    url(r'^network/invitation/accept/$', networkviews.confirm_network_invite, name='confirm_network_invite'),
    url(r'^network/(?P<pk>[0-9]+)/edit/$', networkviews.NetworkUpdateView.as_view(), name='network_edit'),
    url(r'^network/list$', networkviews.NetworkListView.as_view(), name='network_list'),
    url(r'^network/stories$', networkviews.network_stories, name='network_stories'),
    # url(r'^network/stories/json$', networkviews.network_stories_json, name='network_stories_json'),
    url(r'^network/(?P<pk>[0-9]+)/notes/$', noteviews.network_notes, name='network_notes'),
    url(r'^network/(?P<pk>[0-9]+)/note/(?P<note_type>[-\w]+)/content$', noteviews.note_content_html, name='note_content_html'),
    url(r'^network/note/new/$', noteviews.create_network_note, name='create_network_note'),
]
