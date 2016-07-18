from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Browse image',
        help_text='jpg, png, jpeg files only'
    )