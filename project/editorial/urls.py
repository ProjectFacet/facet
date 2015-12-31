from django.conf.urls import url, include

from . import views
# from views import HomeView

urlpatterns = [
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
    url(r'^discussion$', views.discussion, name='discussion'),
    #----------------------------------------------------------------------#
    #   Comment URLS
    #----------------------------------------------------------------------#
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
    #----------------------------------------------------------------------#
    #   User URLS
    #----------------------------------------------------------------------#
    url(r'^user/new/$', views.user_new, name='user_new'),
    url(r'^user/(?P<pk>[0-9]+)/$', views.user_detail, name='user_detail'),
    url(r'^user/(?P<pk>[0-9]+)/edit/$', views.user_edit, name='user_edit'),
    #----------------------------------------------------------------------#
    #   Series URLS
    #----------------------------------------------------------------------#
    url(r'^series/new$', views.series_new, name='series_new'),
    url(r'^series$', views.series_list, name='series_list'),
    url(r'^series/(?P<pk>[0-9]+)/$', views.series_detail, name='series_detail'),
    url(r'^series/(?P<pk>[0-9]+)/edit/$', views.series_edit, name='series_edit'),
    #----------------------------------------------------------------------#
    #   Story URLS
    #----------------------------------------------------------------------#
    url(r'^story/new/$', views.story_new, name='story_new'),
    url(r'^stories$', views.story_list, name='story_list'),
    url(r'^story/(?P<pk>[0-9]+)/$', views.story_detail, name='story_detail'),
    url(r'^story/(?P<pk>[0-9]+)/edit/$', views.story_edit, name='story_edit'),
    #----------------------------------------------------------------------#
    #   Network URLS
    #----------------------------------------------------------------------#
    url(r'^network/new$', views.network_new, name='network_new'),
    url(r'^network/(?P<pk>[0-9]+)/$', views.network_detail, name='network_detail'),
    url(r'^network/(?P<pk>[0-9]+)/edit/$', views.network_edit, name='network_edit'),
    url(r'^network/list$', views.network_list, name='network_list'),
    url(r'^network/stories$', views.network_stories, name='network_stories'),
]
