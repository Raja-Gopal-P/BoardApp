from django.urls import path
from django.urls import re_path
from . import views


app_name = 'Boards'
urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^(?P<pk>\d+)/$', views.board_page, name='board'),
    re_path(r'^(?P<pk>\d+)/new/$', views.new_topic, name='new_topic')
]
