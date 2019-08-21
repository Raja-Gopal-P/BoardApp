from django.urls import path
from django.urls import re_path
from . import views


app_name = 'Boards'
urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^(?P<pk>\d+)/$', views.board_page, name='board'),
    re_path(r'^(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
    re_path(r'^(?P<board_pk>\d+)/topics/(?P<topic_pk>\d+)/$', views.topic_view, name='topic_view'),
    re_path(r'^(?P<board_pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', views.topic_reply, name='topic_reply'),
]
