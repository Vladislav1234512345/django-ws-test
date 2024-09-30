from django.urls import re_path

from . import views

app_name = 'chat'

urlpatterns = [
    re_path(r'^(?P<chat_id>\d+)/$', views.room, name='room'),
    re_path(r'', views.index, name='index'),
]

