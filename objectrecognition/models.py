from __future__ import unicode_literals

from django.db import models

class Document(models.Model):
    docfile = models.ImageField(upload_to = 'documents/',error_messages = {'invalid': ("Image files only")})

class Contact(models.Model):
    firstname = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(max_length = 300)
    phone = models.BigIntegerField()
    message = models.CharField(max_length = 10000)
