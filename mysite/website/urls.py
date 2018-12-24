from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^chat/(?P<name>\w+)/$', views.chat, name='chat'),
    url(r'^show_chat', views.show_chat, name='show_chat'),
    url(r'^base', views.base, name='base'),

]