from django import forms
from .models import EmailContent

class EmailForm(forms.ModelForm):
    class Meta:
        model = EmailContent
        fields = ['task_name', 'subject', 'body', 'to', 'attachment']