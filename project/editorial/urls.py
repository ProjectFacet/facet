from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^story/new/$', views.story_new, name='story_new'),
    url(r'^user/profile/edit/', views.edit_user, name='edit_user')
]
