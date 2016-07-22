from django.contrib import admin

# Register your models here.
from .models import Contact, Document   

class Document(admin.ModelAdmin):
    change_form_template = 'progressbarupload/change_form.html'
    add_form_template = 'progressbarupload/change_form.html'
admin.site.register(Contact,Document)