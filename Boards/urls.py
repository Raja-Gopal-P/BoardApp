from django.urls import path
from django.urls import re_path
from . import views


app_name = 'Boards'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    re_path(r'^(?P<pk>\d+)/$', views.TopicListView.as_view(), name='board'),
    re_path(r'^(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
    re_path(r'^(?P<board_pk>\d+)/topics/(?P<topic_pk>\d+)/$', views.PostListView.as_view(), name='topic_view'),
    re_path(r'^(?P<board_pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', views.topic_reply, name='topic_reply'),
    re_path(r'^(?P<board_pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$', views.EditPost.as_view(),
            name='edit_post'),
]
