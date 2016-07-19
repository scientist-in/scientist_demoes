from django.conf.urls import url, patterns

from django.conf.urls import handler400, handler403, handler404, handler500
#from django.conf.urls.defaults import handler404, handler500
from . import views

handler404 = 'objectrecognition.views.handler404'
urlpatterns = [
    url(r'^objectrecognition/(?P<fromPostFlag>[0-9])/$', 'objectrecognition.views.list', name='list')
    ]
