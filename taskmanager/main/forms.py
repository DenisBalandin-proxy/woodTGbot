from django import forms
from .models import Contact


class UploadFileForm(forms.Form):
    file = forms.FileField(upload_to='your directory name/')