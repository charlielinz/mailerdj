from django import forms
from .models import SendMailEveryFriday

class EmailForm(forms.ModelForm):
    class Meta:
        model = SendMailEveryFriday
        fields = ['subject', 'body', 'to']