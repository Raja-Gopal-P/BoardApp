from django.urls import path
from . import views


app_name = 'Boards'
urlpatterns = [
    path('', views.index, name='index'),
]
