from django.conf.urls import url, patterns

from django.conf.urls import handler400, handler403, handler404, handler500
#from django.conf.urls.defaults import handler404, handler500
from . import views

from django.conf import settings
from django.conf.urls.static import static

handler404 = 'objectrecognition.views.handler404'
urlpatterns = [url(r'contact', 'objectrecognition.views.contact', name='contact'),
    url(r'^objectrecognition/(?P<fromPostFlag>[0-9])/$', 'objectrecognition.views.list', name='list')
    ] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
