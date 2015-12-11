from django.conf.urls import url, include

from . import views

urlpatterns = [
    #----------------------------------------------------------------------#
    #   Homepage URLS
    #----------------------------------------------------------------------#
    url(r'^$', views.index, name='index'),
    #----------------------------------------------------------------------#
    #   Dashboard URLS
    #----------------------------------------------------------------------#
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    #----------------------------------------------------------------------#
    #   Team URLS
    #----------------------------------------------------------------------#
    # url(r'^team$', views.team_list, name='team_list'),
    #----------------------------------------------------------------------#
    #   Discussion URLS
    #----------------------------------------------------------------------#
    # url(r'^discussion$', views.discussion, name='discussion'),
    #----------------------------------------------------------------------#
    #   Organization URLS
    #----------------------------------------------------------------------#
    url(r'^/organization/new$', views.organization_new, name="organization_new"),
    # url(r'^organization/(?P<pk>[0-9]+)/$', views.org_detail, name='organization'),
    # url(r'^organization/(?P<pk>[0-9]+)/edit/$', views.org_edit, name='org_edit'),
    #----------------------------------------------------------------------#
    #   User URLS
    #----------------------------------------------------------------------#
    url(r'^user/(?P<pk>[0-9]+)/$', views.user_detail, name='user_detail'),
    url(r'^user/edit/$', views.user_edit, name='user_edit'),
    #----------------------------------------------------------------------#
    #   Series URLS
    #----------------------------------------------------------------------#
    url(r'^series/new$', views.series_new, name='series_new'),
    # url(r'^series$', views.series_list, name='series_list'),
    # url(r'^series/(?P<pk>[0-9]+)/$', views.series_detail, name='series'),
    # url(r'^series/(?P<pk>[0-9]+)/edit/$', views.series_edit, name='series_edit'),
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
#     url(r'^network/new$', views.network_new, name='network_new')
#     url(r'^network/(?P<pk>[0-9]+)/$', views.network_detail, name='network_detail'),
#     url(r'^network/(?P<pk>[0-9]+)/edit/$', views.network_edit, name='network_edit'),
#     url(r'^network/member$', views.network_member, name'network_member'),
#     url(r'^network/stories$', views.network_stories, name='network_stories'),
]
