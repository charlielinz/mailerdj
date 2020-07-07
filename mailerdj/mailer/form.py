from django import forms
from .models import EmailContent, Library

class EmailForm(forms.ModelForm):
    class Meta:
        model = EmailContent
        exclude = []


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = ['book']