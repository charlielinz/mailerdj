from django import forms
from .models import EmailContent

class EmailForm(forms.ModelForm):
    class Meta:
        model = EmailContent
        fields = ['subject', 'body', 'to', 'attachment']