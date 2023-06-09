from django import forms
from .models import Contact

def getPath():
    return 'C:/Users/Operator11/Desktop/WTG/woodTGbot/wood_export_bot/media/fff.jpg'
class UploadFileForm(forms.Form):
    #file = forms.FileField()
    chat_id = forms.IntegerField(label='chat_id')
    session_id = forms.UUIDField(label='session_id')
    fio = forms.CharField(label='fio', max_length=100)
    benefit = forms.CharField(label='benefit', max_length=100)
    sum = forms.IntegerField(label='sum')
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))