from __future__ import unicode_literals

from django.db import models

class Document(models.Model):
    docfile = models.ImageField(upload_to = 'documents/',error_messages = {'invalid': ("Image files only")})
