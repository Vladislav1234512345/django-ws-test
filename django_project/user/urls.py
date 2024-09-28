from django.urls import re_path
from . import views

app_name = 'user'

urlpatterns = [
    re_path('^login/$', views.login, name='login'),
    re_path('^register/$', views.register, name='register'),
    re_path('^profile/$', views.profile, name='profile'),
    re_path('^logout/$', views.logout, name='logout'),
]