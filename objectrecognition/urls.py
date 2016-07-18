from django.conf.urls import url, patterns

from . import views

urlpatterns = patterns('objectrecognition.views',
    url(r'^objectrecognition/(?P<fromPostFlag>[0-9])/$', 'list', name='list'),
    #url(r'^objectrecognition/$', 'list', name='list'),
)