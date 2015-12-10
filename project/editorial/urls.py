from django.conf.urls import url, include

from . import views

urlpatterns = [
    # homepage
    url(r'^$', views.index, name='index'),
    # user profile
    url(r'^user/profile/edit/', views.edit_user, name='edit_user'),
    # make/edit a series
    url(r'^series/new$', views.series_new, name='series_new'),
    # make/edit a story
    url(r'^story/new/$', views.story_new, name='story_new'),
]
