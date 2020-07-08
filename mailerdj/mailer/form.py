from django import forms
from .models import MailJob, Archive


class EmailForm(forms.ModelForm):
    class Meta:
        model = MailJob
        exclude = []


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Archive
        fields = ['archive']
