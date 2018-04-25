""" Forms for editorial app. """

from django.conf.urls import url, include
from django.http import HttpResponse

from views import (
    accounts,
    assets,
    contractors,
    discussion,
    downloads,
    events,
    facet,
    general,
    inbox,
    networks,
    notes,
    organizations,
    platforms,
    projects,
    pushcontent,
    schedules,
    series,
    story,
    tasks,
    users,
    )

from django.views import generic

from . import api

from views.search import EditorialSearchView

urlpatterns = [
    # robots
    url(r'^robots.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),


    url(r'test/$', generic.TemplateView.as_view(template_name='editorial/test.html')),

    #   Account URLS
    url(r'^account/selection/$', accounts.AccountSelectionView.as_view(), name='account_selection'),

    #   API URL - Used API endpoints
    url('^api/', include(api.router.urls)),

    #   Facet to WordPress URL - On demand pushing
    url(r'^facet/json/$', pushcontent.facet_json, name='facet_json'),
    # url(r'^facet/wordpress/$', pushcontentviews.push_facet_wp, name='push_facet_wp'),

    #   Homepage URLS
    url(r'^$', general.LandingTemplateView.as_view(), name='index'),

    #   Dashboard URLS
    url(r'^dashboard/$', general.DashboardTemplateView.as_view(), name='dashboard'),

    #   Schedule URLS
    url(r'^schedule/$', schedules.schedule, name='schedule'),
    url(r'^schedulecontent/$', schedules.schedule_content, name='schedule-content'),

    #   Asset Library URLS
    url(r'^assets/$', assets.AssetLibraryTemplateView.as_view(), name='asset_library'),
    url(r'^assets/images/$', assets.ImageAssetLibraryTemplateView.as_view(), name='image_asset_list'),
    url(r'^assets/image/(?P<pk>\d+)/$', assets.ImageAssetUpdateView.as_view(), name='image_asset_detail'),
    url(r'^assets/image/(?P<pk>\d+)/delete/$', assets.ImageAssetDeleteView.as_view(), name='image_asset_delete'),
    url(r'^assets/image/(?P<image>\d+)/facet/(?P<facet>\d+)/remove/$', assets.ImageAssetDisassociateView.as_view(), name='image_asset_remove'),

    url(r'^assets/documents/$', assets.DocumentAssetLibraryTemplateView.as_view(), name='document_asset_list'),
    url(r'^assets/document/(?P<pk>\d+)/$', assets.DocumentAssetUpdateView.as_view(), name='document_asset_detail'),
    url(r'^assets/document/(?P<pk>\d+)/delete/$', assets.DocumentAssetDeleteView.as_view(), name='document_asset_delete'),
    url(r'^assets/document/(?P<document>\d+)/facet/(?P<facet>\d+)/remove/$', assets.DocumentAssetDisassociateView.as_view(), name='document_asset_remove'),

    url(r'^assets/audio/$', assets.AudioAssetLibraryTemplateView.as_view(), name='audio_asset_list'),
    url(r'^assets/audio/(?P<pk>\d+)/$', assets.AudioAssetUpdateView.as_view(), name='audio_asset_detail'),
    url(r'^assets/audio/(?P<pk>\d+)/delete/$', assets.AudioAssetDeleteView.as_view(), name='audio_asset_delete'),
    url(r'^assets/audio/(?P<audio>\d+)/facet/(?P<facet>\d+)/remove/$', assets.AudioAssetDisassociateView.as_view(), name='audio_asset_remove'),

    url(r'^assets/video/$', assets.VideoAssetLibraryTemplateView.as_view(), name='video_asset_list'),
    url(r'^assets/video/(?P<pk>\d+)/$', assets.VideoAssetUpdateView.as_view(), name='video_asset_detail'),
    url(r'^assets/video/(?P<pk>\d+)/delete/$', assets.VideoAssetDeleteView.as_view(), name='video_asset_delete'),
    url(r'^assets/video/(?P<video>\d+)/facet/(?P<facet>\d+)/remove/$', assets.VideoAssetDisassociateView.as_view(), name='video_asset_remove'),

    #   Collaborations URLS
    url(r'^collaborations/$', general.CollaborationTemplateView.as_view(), name='collaborations'),

    #   Team URLS
    url(r'^team/$', general.TeamTemplateView.as_view(), name='team_list'),

    #   Inbox URLS - Labeled as Inbox in navigation
    url(r'^inbox/$', inbox.Inbox.as_view(), name='inbox'),
    url(r'^inbox/sent/$', inbox.SentMessages.as_view(), name='sent_html'),
    url(r'^inbox/(?P<comment_type>[-\w]+)/comments/$', inbox.CommentList.as_view(), name='comments_html'),
    # url(r'^inbox/important/$', inboxviews.inbox_important, name='inbox_important'),
    # url(r'^inbox/trash/$', inboxviews.inbox_trash, name='inbox_trash'),

    #   Private Message URLS
    url(r'^privatemessage/compose/$', inbox.PrivateMessageCompose.as_view(), name='privatemessage_compose'),
    url(r'^privatemessage/compose-modal/$', inbox.PrivateMessageComposeModal.as_view(), name='privatemessage_compose_modal'),
    url(r'^privatemessage/compose-modal-success/$', generic.TemplateView.as_view(template_name='editorial/privatemessage_compose_modal_success.html'), name='privatemessage_compose_modal_success'),

    url(r'^privatemessage/(?P<pk>\d+)/content/$', inbox.MessageContent.as_view(), name='message_html'),

    #   Copy URLS
    url(r'^story/(?P<story>\d+)/copy/$', networks.CopyNetworkStoryView.as_view(), name='copy_network_story'),

    #   Download URLS
    url(r'^story/(?P<pk>\d+)/select-download/$', downloads.StoryDownloadTemplateView.as_view(), name='story_download_form'),
    url(r'^story/(?P<pk>\d+)/download/$', downloads.StoryDownloadProcessView.as_view(), name='create_download'),

    #   Search URLS
    url(r"^search/$", EditorialSearchView.as_view(), name="search"),

    #   Comment URLS
    url(r'^organization/comment/new/$', discussion.CommentCreateView.as_view(), name='create_orgcomment'),
    url(r'^network/comment/new/$', discussion.CommentCreateView.as_view(), name='create_networkcomment'),
    url(r'^project/comment/new/$', discussion.CommentCreateView.as_view(), name='create_projectcomment'),
    url(r'^series/comment/new/$', discussion.CommentCreateView.as_view(), name='create_seriescomment'),
    url(r'^story/comment/new/$', discussion.CommentCreateView.as_view(), name='create_storycomment'),
    url(r'^facet/comment/new/$', discussion.CommentCreateView.as_view(), name='create_facetcomment'),
    url(r'^task/comment/new/$', discussion.CommentCreateView.as_view(), name='create_taskcomment'),
    url(r'^event/comment/new/$', discussion.CommentCreateView.as_view(), name='create_eventcomment'),
    url(r'^assignment/comment/new/$', discussion.CommentCreateView.as_view(), name='create_assignmentcomment'),

    #   Note URLS
    url(r'^organization/note/new/$', notes.NoteCreateView.as_view(), name='create_orgnote'),
    url(r'^user/note/new/$', notes.NoteCreateView.as_view(), name='create_usernote'),
    url(r'^network/note/new/$', notes.NoteCreateView.as_view(), name='create_networknote'),
    url(r'^projectnote/new/$', notes.NoteCreateView.as_view(), name='create_projectnote'),
    url(r'^series/note/new/$', notes.NoteCreateView.as_view(), name='create_seriesnote'),
    url(r'^story/note/new/$', notes.NoteCreateView.as_view(), name='create_storynote'),
    url(r'^facet/note/new/$', notes.NoteCreateView.as_view(), name='create_facetnote'),
    url(r'^task/note/new/$', notes.NoteCreateView.as_view(), name='create_tasknote'),
    url(r'^event/note/new/$', notes.NoteCreateView.as_view(), name='create_eventnote'),
    url(r'^note/(?P<pk>\d+)/delete/$', notes.NoteDelete.as_view(), name='note_delete'),
    # url(r'^assignment/note/new/$', noteviews.NoteCreateView.as_view(), name='create_assignmentnote'),

    #   Platform URLS
    url(r'^user/(?P<pk>\d+)/platformaccounts/edit/$', platforms.UserPlatformAccountCreateView.as_view(), name='user_platformaccounts_create'),
    # url(r'^organization/(?P<pk>\d+)/platformaccounts/edit/$', platformviews.organization_platformaccounts_create, name='organization_platformaccounts_create'),
    # url(r'^project/(?P<pk>\d+)/platformaccounts/edit/$', platformviews.project_platformaccounts_create, name='project_platformaccounts_create'),

    #   Organization URLS
    url(r'^organization/new/$', organizations.OrganizationCreateView.as_view(), name="org_new"),
    url(r'^organization/(?P<pk>\d+)/$', organizations.OrganizationDetailView.as_view(), name='org_detail'),
    url(r'^organization/(?P<pk>\d+)/edit/$', organizations.OrganizationUpdateView.as_view(), name='org_edit'),
    url(r'^organization/(?P<pk>\d+)/notes/$', notes.OrganizationNoteView.as_view(), name='org_notes'),
    url(r'^organization/(?P<org>\d+)/note/(?P<note>\d+)/content/$', notes.NoteContent.as_view(), name='org_note_content'),
    # url(r'^organization/(?P<pk>\d+)/comments/$', communicationviews.org_comments, name='org_comments'),
    url(r'^organization/(?P<pk>\d+)/facet/json/$', pushcontent.OrganizationFacetJSONView.as_view(), name='org_facet_json'),


    #   User URLS
    url(r'^user/new/$', users.UserCreateView.as_view(), name='user_new'),
    url(r'^user/(?P<pk>\d+)/$', users.UserDetailView.as_view(), name='user_detail'),
    url(r'^user/(?P<pk>\d+)/edit/$', users.UserUpdateView.as_view(), name='user_edit'),
    url(r'^user/(?P<pk>\d+)/notes/$', notes.UserNoteView.as_view(), name='user_notes'),
    url(r'^user/(?P<user>\d+)/note/(?P<note>\d+)/content/$', notes.NoteContent.as_view(), name='user_note_content'),
    url(r'^user/deactivate/$', users.UserDeactivateView.as_view(), name='user_deactivate'),
    url(r'^user/activate/$', users.UserActivateView.as_view(), name='user_activate'),

    #   Contractor URLS
    url(r'^contractor/new/$', contractors.ContractorCreateView.as_view(), name='contractor_new'),
    url(r'^contractor/(?P<pk>\d+)/$', contractors.ContractorDetailView.as_view(), name='contractor_detail'),
    url(r'^contractor/(?P<pk>\d+)/edit/$', contractors.ContractorUpdateView.as_view(), name='contractor_edit'),
    url(r'^contractor/(?P<pk>\d+)/calls/$', contractors.CallListView.as_view(), name='contractor_calls'),
    url(r'^contractor/(?P<pk>\d+)/pitches/$', contractors.PitchListView.as_view(), name='contractor_pitches'),
    url(r'^contractor/list/$', contractors.PublicContractorListView.as_view(), name='public_contractor_list'),
    url(r'^contractor/pool/$', contractors.AffiliationListView.as_view(), name='affiliation_list'),
    url(r'^contractor/pool/add/$', contractors.AffiliationCreateView.as_view(), name='affiliation_new'),
    url(r'^contractor/pool/(?P<pk>\d+)/$', contractors.AffiliationDetailView.as_view(), name='affiliation_detail'),
    url(r'^contractor/pool/(?P<pk>\d+)/edit/$', contractors.AffiliationUpdateView.as_view(), name='affiliation_edit'),
    url(r'^talenteditor/list/$', contractors.PublicTalentEditorListView.as_view(), name='public_editor_list'),
    url(r'^talenteditor/(?P<pk>\d+)/$', contractors.PublicTalentEditorDetailView.as_view(), name='talent_editor_detail'),
    url(r'^talenteditor/(?P<pk>\d+)/dashboard/$', contractors.PublicTalentEditorDashboardView.as_view(), name='talent_editor_dashboard'),
    url(r'^assignment/new/$', contractors.AssignmentCreateView.as_view(), name='assignment_new'),
    url(r'^assignments/$', contractors.AssignmentListView.as_view(), name='assignment_list'),
    url(r'^assignment/(?P<pk>\d+)/$', contractors.AssignmentDetailView.as_view(), name='assignment_detail'),
    url(r'^assignment/(?P<pk>\d+)/edit/$', contractors.AssignmentUpdateView.as_view(), name='assignment_edit'),
    url(r'^assignment/(?P<pk>\d+)/delete/$', contractors.AssignmentDeleteView.as_view(), name='assignment_delete'),
    url(r'^call/new/$', contractors.CallCreateView.as_view(), name='call_new'),
    url(r'^calls/$', contractors.CallListView.as_view(), name='call_list'),
    url(r'^call/(?P<pk>\d+)/$', contractors.CallDetailView.as_view(), name='call_detail'),
    url(r'^call/(?P<pk>\d+)/edit/$', contractors.CallUpdateView.as_view(), name='call_edit'),
    url(r'^call/(?P<pk>\d+)/delete/$', contractors.CallDeleteView.as_view(), name='call_delete'),
    url(r'^pitch/new/$', contractors.PitchCreateView.as_view(), name='pitch_new'),
    url(r'^pitches/$', contractors.PitchListView.as_view(), name='pitch_list'),
    url(r'^pitch/(?P<pk>\d+)/$', contractors.PitchDetailView.as_view(), name='pitch_detail'),
    url(r'^pitch/(?P<pk>\d+)/edit/$', contractors.PitchUpdateView.as_view(), name='pitch_edit'),
    url(r'^pitch/(?P<pk>\d+)/delete/$', contractors.PitchDeleteView.as_view(), name='pitch_delete'),

    #   Project URLS
    url(r'^project/new/$', projects.ProjectCreateView.as_view(), name='project_new'),
    url(r'^projects/$', projects.ProjectListView.as_view(), name='project_list'),
    url(r'^project/(?P<pk>\d+)/$', projects.ProjectDetailView.as_view(), name='project_detail'),
    url(r'^project/(?P<pk>\d+)/edit/$', projects.ProjectUpdateView.as_view(), name='project_edit'),
    url(r'^project/(?P<pk>\d+)/delete/$', projects.ProjectDeleteView.as_view(), name='project_delete'),
    url(r'^project/(?P<pk>\d+)/notes/$', notes.ProjectNoteView.as_view(), name='project_notes'),
    url(r'^project/(?P<project>\d+)/note/(?P<note>\d+)/content$', notes.NoteContent.as_view(), name='project_note_content'),
    url(r'^project/(?P<pk>\d+)/schedule/$', projects.ProjectSchedule.as_view(), name='project_schedule'),
    url(r'^project/(?P<pk>\d+)/assets/$', projects.ProjectAssetTemplateView.as_view(), name='project_assets'),
    url(r'^project/(?P<pk>\d+)/stories/$', projects.ProjectStoryTemplateView.as_view(), name='project_stories'),
    url(r'^project/(?P<pk>\d+)/team/edit/$', projects.ProjectTeamUpdateView.as_view(), name='project_team_edit'),

    #   Series URLS
    url(r'^series/new/$', series.SeriesCreateView.as_view(), name='series_new'),
    url(r'^series/$', series.SeriesListView.as_view(), name='series_list'),
    url(r'^series/json/$', series.series_json, name='series_json'),
    url(r'^series/(?P<pk>\d+)/$', series.SeriesDetailView.as_view(), name='series_detail'),
    url(r'^series/(?P<pk>\d+)/edit/$', series.SeriesUpdateView.as_view(), name='series_edit'),
    url(r'^series/(?P<pk>\d+)/delete/$', series.SeriesDeleteView.as_view(), name='series_delete'),
    url(r'^series/(?P<pk>\d+)/assets/$', series.SeriesAssetTemplateView.as_view(), name='series_assets'),
    url(r'^series/(?P<pk>\d+)/schedule/$', series.SeriesSchedule.as_view(), name='series_schedule'),
    url(r'^series/(?P<pk>\d+)/notes/$', notes.SeriesNoteView.as_view(), name='series_notes'),
    url(r'^series/(?P<series>\d+)/note/(?P<note>\d+)/content/$', notes.NoteContent.as_view(), name='series_note_content'),
    url(r'^series/(?P<pk>\d+)/team/edit/$', series.SeriesTeamUpdateView.as_view(), name='series_team_edit'),

    #   Story URLS
    url(r'^story/new/$', story.StoryCreateView.as_view(), name='story_new'),
    url(r'^stories/$', story.StoryListView.as_view(), name='story_list'),
    url(r'^story/(?P<pk>\d+)/$', story.StoryDetailView.as_view(), name='story_detail'),
    url(r'^story/(?P<pk>\d+)/edit/$', story.StoryUpdateView.as_view(), name='story_edit'),
    url(r'^story/(?P<pk>\d+)/delete/$', story.StoryDeleteView.as_view(), name='story_delete'),
    url(r'^story/(?P<pk>\d+)/schedule/$', story.StorySchedule.as_view(), name='story_schedule'),
    url(r'^story/(?P<pk>\d+)/notes/$', notes.StoryNoteView.as_view(), name='story_notes'),
    url(r'^story/(?P<story>\d+)/note/(?P<note>\d+)/content/$', notes.NoteContent.as_view(), name='story_note_content'),
    url(r'^story/(?P<pk>\d+)/team/edit/$', story.StoryTeamUpdateView.as_view(), name='story_team_edit'),
    # url(r'^story/(?P<pk>\d+)/team/json/$', story.story_team_options_json, name='story_team_options_json'),

    #   Facet URLS
    url(r'^story/(?P<story>\d+)/facet/add/$', facet.FacetPreCreateView.as_view(), name="facet_precreate"),
    url(r'^story/(?P<story>\d+)/facet/add/(?P<template_id>\d+)/$', facet.FacetCreateView.as_view(), name="facet_add"),
    url(r'^story/(?P<story>\d+)/facet/(?P<pk>\d+)/edit/$', facet.FacetUpdateView.as_view(), name="facet_edit"),
    url(r'^story/(?P<story>\d+)/facet/(?P<pk>\d+)/delete/$', facet.FacetDeleteView.as_view(), name="facet_delete"),
    # Facet templates
    url(r'^organization/(?P<org>\d+)/facet/templates/$', facet.FacetTemplateListView.as_view(), name="facet_template_list"),
    url(r'^organization/(?P<org>\d+)/facet/templates/create/$', facet.FacetTemplateCreateView.as_view(), name="facet_template_create"),
    url(r'^organization/basic/facet/templates/(?P<template>\d+)/$', facet.FacetTemplateDetailView.as_view(), name="facet_template_detail"),
    url(r'^organization/(?P<org>\d+)/facet/templates/(?P<template>\d+)/edit/$', facet.FacetTemplateUpdateView.as_view(), name="facet_template_edit"),
    url(r'^organization/(?P<org>\d+)/facet/templates/(?P<template>\d+)/delete/$', facet.FacetTemplateDeleteView.as_view(), name="facet_template_delete"),

    #   Task URLS
    url(r'^task/new/$', tasks.TaskCreateView.as_view(), name='task_new'),
    url(r'^task/(?P<pk>\d+)/$', tasks.TaskUpdateView.as_view(), name='task_detail'),
    url(r'^task/(?P<pk>\d+)/notes/$', notes.TaskNoteView.as_view(), name='task_notes'),
    url(r'^task/(?P<pk>\d+)/delete/$', tasks.TaskDeleteView.as_view(), name='task_delete'),
    url(r'^task/(?P<task>\d+)/note/(?P<note>\d+)/content/$', notes.NoteContent.as_view(), name='task_note_content'),
    url(r'^project/(?P<pk>\d+)/tasks/$', tasks.ProjectTaskView.as_view(), name='project_task_list'),
    url(r'^series/(?P<pk>\d+)/tasks/$', tasks.SeriesTaskView.as_view(), name='series_task_list'),
    url(r'^story/(?P<pk>\d+)/tasks/$', tasks.StoryTaskView.as_view(), name='story_task_list'),
    url(r'^event/(?P<pk>\d+)/tasks/$', tasks.EventTaskView.as_view(), name='event_task_list'),

    #   Event URLS
    url(r'^event/new/$', events.EventCreateView.as_view(), name='event_new'),
    url(r'^event/(?P<pk>\d+)/$', events.EventUpdateView.as_view(), name='event_detail'),
    url(r'^event/(?P<pk>\d+)/notes/$', notes.EventNoteView.as_view(), name='event_notes'),
    url(r'^event/(?P<pk>\d+)/delete/$', events.EventDeleteView.as_view(), name='event_delete'),
    url(r'^event/(?P<event>\d+)/note/(?P<note>\d+)/content/$', notes.NoteContent.as_view(), name='event_note_content'),
    url(r'^organization/(?P<pk>\d+)/events/$', events.OrganizationEventView.as_view(), name='organization_event_list'),
    url(r'^project/(?P<pk>\d+)/events/$', events.ProjectEventView.as_view(), name='project_event_list'),
    url(r'^project/(?P<pk>\d+)/events/schedule/$', events.ProjectEventSchedule.as_view(), name='project_event_schedule'),
    url(r'^series/(?P<pk>\d+)/events/$', events.SeriesEventView.as_view(), name='series_event_list'),
    url(r'^series/(?P<pk>\d+)/events/schedule/$', events.SeriesEventSchedule.as_view(), name='series_event_schedule'),
    url(r'^story/(?P<pk>\d+)/events/$', events.StoryEventView.as_view(), name='story_event_list'),
    url(r'^story/(?P<pk>\d+)/events/schedule$', events.StoryEventSchedule.as_view(), name='story_event_schedule'),

    #   Asset URLS

    # Images
    url(r'^image/new/$', assets.ImageAssetCreateView.as_view(), name='upload_image'),
    url(r'^story/(?P<story>\d+)/facet/(?P<facet>\d+)/images/add/$', assets.LibraryImageAssociateView.as_view(), name='libraryimage_add'),
    # Documents
    url(r'^document/new/$', assets.DocumentAssetCreateView.as_view(), name='upload_document'),
    url(r'^story/(?P<story>\d+)/facet/(?P<facet>\d+)/documents/add/$', assets.LibraryDocumentAssociateView.as_view(), name='librarydocument_add'),
    # Audio
    url(r'^audio/new/$', assets.AudioAssetCreateView.as_view(), name='upload_audio'),
    url(r'^story/(?P<story>\d+)/facet/(?P<facet>\d+)/audio/add/$', assets.LibraryAudioAssociateView.as_view(), name='libraryaudio_add'),
    # Video
    url(r'^video/new/$', assets.VideoAssetCreateView.as_view(), name='upload_video'),
    url(r'^story/(?P<story>\d+)/facet/(?P<facet>\d+)/video/add/$', assets.LibraryVideoAssociateView.as_view(), name='libraryvideo_add'),

    # Simple Images
    url(r'^organization/(?P<org>\d+)/internalassets/$', assets.SimpleAssetLibraryTemplateView.as_view(), name='simple_asset_library'),
    url(r'^organization/(?P<org>\d+)/internalassets/images/$', assets.SimpleImageAssetLibraryTemplateView.as_view(), name='simple_image_asset_library'),
    url(r'^organization/(?P<org>\d+)/internalassets/documents/$', assets.SimpleDocumentAssetLibraryTemplateView.as_view(), name='simple_document_asset_library'),
    url(r'^organization/(?P<org>\d+)/internalassets/audio/$', assets.SimpleAudioAssetLibraryTemplateView.as_view(), name='simple_audio_asset_library'),
    url(r'^organization/(?P<org>\d+)/internalassets/video/$', assets.SimpleVideoAssetLibraryTemplateView.as_view(), name='simple_video_asset_library'),

    url(r'^internalassets/simpleimage/new/$', assets.SimpleImageCreateView.as_view(), name='upload_simple_image'),
    url(r'^internalassets/simpleimage/add/$', assets.SimpleImageLibraryAssociateView.as_view(), name='library_simpleimage_add'),
    url(r'^internalassets/simpleimage/(?P<pk>\d+)/$', assets.SimpleImageUpdateView.as_view(), name='simple_image_detail'),
    url(r'^internalassets/simpleimage/(?P<pk>\d+)/delete/$', assets.SimpleImageAssetDeleteView.as_view(), name='simple_image_delete'),
    url(r'^internalassets/simpleimage/(?P<simpleimage>\d+)/remove/$', assets.SimpleImageAssetDisassociateView.as_view(), name='simple_image_remove'),
    # Simple documents
    url(r'^internalassets/simpledocument/new/$', assets.SimpleDocumentCreateView.as_view(), name='upload_simple_document'),
    url(r'^internalassets/simpledocument/add/$', assets.SimpleDocumentLibraryAssociateView.as_view(), name='library_simpledocument_add'),
    url(r'^internalassets/simpledocument/(?P<pk>\d+)/$', assets.SimpleDocumentUpdateView.as_view(), name='simple_document_detail'),
    url(r'^internalassets/simpledocument/(?P<pk>\d+)/delete/$', assets.SimpleDocumentAssetDeleteView.as_view(), name='simple_document_delete'),
    url(r'^internalassets/simpledocument/(?P<simpledocument>\d+)/remove/$', assets.SimpleDocumentAssetDisassociateView.as_view(), name='simple_document_remove'),
    # Simple Audio
    url(r'^internalassets/simpleaudio/new/$', assets.SimpleAudioCreateView.as_view(), name='upload_simple_audio'),
    url(r'^internalassets/simpleaudio/add/$', assets.SimpleAudioLibraryAssociateView.as_view(), name='library_simpleaudio_add'),
    url(r'^internalassets/simpleaudio/(?P<pk>\d+)/$', assets.SimpleAudioUpdateView.as_view(), name='simple_audio_detail'),
    url(r'^internalassets/simpleaudio/(?P<pk>\d+)/delete/$', assets.SimpleAudioAssetDeleteView.as_view(), name='simple_audio_delete'),
    url(r'^internalassets/simpleaudio/(?P<simpleaudio>\d+)/remove/$', assets.SimpleAudioAssetDisassociateView.as_view(), name='simple_audio_remove'),
    # Simple Video
    url(r'^internalassets/simplevideo/new/$', assets.SimpleVideoCreateView.as_view(), name='upload_simple_video'),
    url(r'^internalassets/simplevideo/add/$', assets.SimpleVideoLibraryAssociateView.as_view(), name='library_simplevideo_add'),
    url(r'^internalassets/simplevideo/(?P<pk>\d+)/$', assets.SimpleVideoUpdateView.as_view(), name='simple_video_detail'),
    url(r'^internalassets/simplevideo/(?P<pk>\d+)/delete/$', assets.SimpleVideoAssetDeleteView.as_view(), name='simple_video_delete'),
    url(r'^internalassets/simplevideo/(?P<simplevideo>\d+)/remove/$', assets.SimpleVideoAssetDisassociateView.as_view(), name='simple_video_remove'),

    #   Network URLS
    url(r'^network/new/$', networks.NetworkCreateView.as_view(), name='network_new'),
    url(r'^network/(?P<pk>\d+)/$', networks.NetworkDetailView.as_view(), name='network_detail'),
    url(r'^network/(?P<pk>\d+)/invitation/$', networks.NetworkInvitationSend.as_view(), name='network_invitation_send'),
    url(r'^network/(?P<pk>\d+)/invitation/accept/$', networks.NetworkInvitationAccept.as_view(), name='network_invitation_accept'),
    url(r'^network/(?P<pk>\d+)/edit/$', networks.NetworkUpdateView.as_view(), name='network_edit'),
    url(r'^network/list/$', networks.NetworkListView.as_view(), name='network_list'),
    url(r'^network/stories/$', networks.NetworkStoryListView.as_view(), name='network_stories'),
    # url(r'^network/stories/json/$', networkviews.network_stories_json, name='network_stories_json'),
    url(r'^network/(?P<pk>\d+)/notes/$', notes.NetworkNoteView.as_view(), name='network_notes'),
    url(r'^network/(?P<network>\d+)/note/(?P<note>\d+)/content/$', notes.NoteContent.as_view(), name='network_note_content'),
]
