from django.conf.urls import url

from . import views

pk = '(?P<link_pk>[0-9]+)'

urlpatterns = [
    #url(regex, view, kwargs, name, prefix)
    url(r'^$', views.index, name='home'),
    url(r'^index[/]{0,1}$', views.index, name='index'),
    url(r'^control[/]{0,1}$', views.control, name='control'),
    url(r'^templates[/]{0,1}$', views.templates, name='templates'),
    url(r'^upload[/]{0,1}$', views.upload, name='upload'),
    url(r'^autotemplates[/]{0,1}$', views.autotemplates, name='autotemplates'),
    url(r'^start/'+pk+'[/]{0,1}$', views.start, name='start'),
    url(r'^stop/'+pk+'[/]{0,1}$', views.stop, name='stop'),
    url(r'^restart/'+pk+'[/]{0,1}$', views.restart, name='restart'),
    url(r'^status/'+pk+'[/]{0,1}$', views.status, name='status'),
    url(r'^sync/'+pk+'[/]{0,1}$', views.sync, name='sync'),
]