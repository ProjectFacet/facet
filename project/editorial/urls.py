""" Forms for editorial app. """

from django.conf.urls import url, include

from . import views
# from views import HomeView

urlpatterns = [
    #----------------------------------------------------------------------#
    #   Test URL - Used for non-destructive testing of templates/queries
    #----------------------------------------------------------------------#
    url(r'^test$', views.test, name='test'),
    #----------------------------------------------------------------------#
    #   Homepage URLS
    #----------------------------------------------------------------------#
    url(r'^$', views.index, name='index'),
    # url(r'^$', HomeView.as_view(), name='index'),
    #----------------------------------------------------------------------#
    #   Dashboard URLS
    #----------------------------------------------------------------------#
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    #----------------------------------------------------------------------#
    #   Collaborations URLS
    #----------------------------------------------------------------------#
    url(r'^collaborations$', views.collaborations, name='collaborations'),
    #----------------------------------------------------------------------#
    #   Team URLS
    #----------------------------------------------------------------------#
    url(r'^team$', views.team_list, name='team_list'),
    #----------------------------------------------------------------------#
    #   Discussion URLS
    #----------------------------------------------------------------------#
    # Labeled as Inbox in navigation
    url(r'^discussion$', views.discussion, name='discussion'),
    #----------------------------------------------------------------------#
    #   Private Message URLS
    #----------------------------------------------------------------------#
    url(r'^privatemessage/new/$', views.private_message_new, name='private_message_new'),
    #----------------------------------------------------------------------#
    #   Comment URLS
    #----------------------------------------------------------------------#
    url(r'^organizationcomment/new$', views.create_orgcomment, name='create_orgcomment'),
    url(r'^networkcomment/new$', views.create_networkcomment, name='create_networkcomment'),
    url(r'^seriescomment/new$', views.create_seriescomment, name='create_seriescomment'),
    url(r'^storycomment/new$', views.create_storycomment, name='create_storycomment'),
    url(r'^webcomment/new$', views.create_webcomment, name='create_webcomment'),
    url(r'^printcomment/new$', views.create_printcomment, name='create_printcomment'),
    url(r'^audiocomment/new$', views.create_audiocomment, name='create_audiocomment'),
    url(r'^videocomment/new$', views.create_videocomment, name='create_videocomment'),
    #----------------------------------------------------------------------#
    #   Organization URLS
    #----------------------------------------------------------------------#
    url(r'^/organization/new$', views.org_new, name="org_new"),
    url(r'^organization/(?P<pk>[0-9]+)/$', views.org_detail, name='org_detail'),
    url(r'^organization/(?P<pk>[0-9]+)/edit/$', views.org_edit, name='org_edit'),
    url(r'^organization/(?P<pk>[0-9]+)/notes/$', views.organization_notes, name='organization_notes'),
    url(r'^organization/note/new/$', views.create_organization_note, name='create_organization_note'),
    #----------------------------------------------------------------------#
    #   User URLS
    #----------------------------------------------------------------------#
    url(r'^user/new/$', views.user_new, name='user_new'),
    url(r'^user/(?P<pk>[0-9]+)/$', views.user_detail, name='user_detail'),
    url(r'^user/(?P<pk>[0-9]+)/edit/$', views.user_edit, name='user_edit'),
    url(r'^user/(?P<pk>[0-9]+)/notes/$', views.user_notes, name='user_notes'),
    url(r'^user/note/new/$', views.create_user_note, name='create_user_note'),
    #----------------------------------------------------------------------#
    #   Series URLS
    #----------------------------------------------------------------------#
    url(r'^series/new/$', views.series_new, name='series_new'),
    url(r'^series$', views.series_list, name='series_list'),
    url(r'^series/(?P<pk>[0-9]+)/$', views.series_detail, name='series_detail'),
    url(r'^series/(?P<pk>[0-9]+)/edit/$', views.series_edit, name='series_edit'),
    url(r'^series/(?P<pk>[0-9]+)/notes/$', views.series_notes, name='series_notes'),
    url(r'^series/note/new/$', views.create_series_note, name='create_series_note'),
    #----------------------------------------------------------------------#
    #   Story URLS
    #----------------------------------------------------------------------#
    url(r'^story/new/$', views.story_new, name='story_new'),
    url(r'^stories$', views.story_list, name='story_list'),
    url(r'^story/(?P<pk>[0-9]+)/$', views.story_detail, name='story_detail'),
    url(r'^story/(?P<pk>[0-9]+)/edit/$', views.story_edit, name='story_edit'),
    url(r'^story/note/new/$', views.create_story_note, name='create_story_note'),
    #----------------------------------------------------------------------#
    #   Asset URLS
    #----------------------------------------------------------------------#
    url(r'^webfacet/image/new/$', views.upload_webfacet_image, name='upload_webfacet_image'),
    url(r'^printfacet/image/new/$', views.upload_printfacet_image, name='upload_printfacet_image'),
    url(r'^audiofacet/image/new/$', views.upload_audiofacet_image, name='upload_audiofacet_image'),
    url(r'^videofacet/image/new/$', views.upload_videofacet_image, name='upload_videofacet_image'),
    url(r'^webfacet/image/add/$', views.add_webfacet_image, name='add_webfacet_image'),
    # url(r'^printfacet/image/add/$', views.add_printfacet_image, name='add_printfacet_image'),
    # url(r'^audiofacet/image/add/$', views.add_audiofacet_image, name='add_audiofacet_image'),
    # url(r'^videofacet/image/add/$', views.add_videofacet_image, name='add_videofacet_image'),
    #----------------------------------------------------------------------#
    #   Network URLS
    #----------------------------------------------------------------------#
    url(r'^network/new/$', views.network_new, name='network_new'),
    url(r'^network/(?P<pk>[0-9]+)/$', views.network_detail, name='network_detail'),
    url(r'^network/invitation/$', views.send_network_invite, name='send_network_invite'),
    url(r'^network/invitation/accept/$', views.confirm_network_invite, name='confirm_network_invite'),
    url(r'^network/(?P<pk>[0-9]+)/edit/$', views.network_edit, name='network_edit'),
    url(r'^network/list$', views.network_list, name='network_list'),
    url(r'^network/stories$', views.network_stories, name='network_stories'),
    url(r'^network/(?P<pk>[0-9]+)/notes/$', views.network_notes, name='network_notes'),
    url(r'^network/note/new/$', views.create_network_note, name='create_network_note'),
    #----------------------------------------------------------------------#
    #   Copy URLS
    #----------------------------------------------------------------------#
    url(r'^story/copy/(?P<pk>[0-9]+)/$', views.copy_network_story, name='copy_network_story'),
]
