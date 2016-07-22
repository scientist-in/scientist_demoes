from django import forms

class DocumentForm(forms.Form):
    docfile = forms.ImageField(
        label='Browse image',
        help_text='jpg, png, jpeg only'
    )
class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    contact_message = forms.CharField(
        required=True,
        widget=forms.Textarea
    )