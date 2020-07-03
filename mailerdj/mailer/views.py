from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import EmailContent
from .form import EmailForm
from win32com import client
import schedule
import time
import os
import json


def index(request):
    emailcontents = EmailContent.objects.all()
    context = {
        'objects': emailcontents
    }
    return render(request, 'mailer/index.html', context)


def send_mail(subject, body, to, cc='', bcc='', attachments=[], just_show=False):
    """
    The method of sending Email by outlook.
    """

    olMailItem = 0x0
    outlook_client = client.Dispatch("Outlook.Application")
    mail = outlook_client.CreateItem(olMailItem)
    mail.Subject = subject
    mail.Body = body
    mail.To = to
    if cc:
        mail.CC = cc
    if bcc:
        mail.BCC = bcc
    if attachments:
        for attachment in attachments:
            mail.Attachments.Add(attachment)
    if just_show:
        mail.display()
    else:
        mail.Send()


def add_detail(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/mailer/')
        context = {
            'form': form
        }
        return render(request, 'mailer/add_detail.html', context)
    else:
        form = EmailForm()
        context = {
            'form': form
        }
        return render(request, 'mailer/add_detail.html', context)


def edit_detail(request, id):
    instance = get_object_or_404(klass=EmailContent, pk=id)
    if request.method == 'POST':
        form = EmailForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('/mailer')
        context = {
            'form': form
        }
        return render(request, 'mailer/edit_detail.html', context)
    else:
        form = EmailForm(instance=instance)
        context = {
            'form': form
        }
        return render(request, 'mailer/edit_detail.html', context)


def delete_detail(request, id):
    if request.method == 'POST':
        try:
            emailcontent = EmailContent.objects.get(id=id)
        except EmailContent.DoesNotExist:
            raise Http404('Page do not exist')
        emailcontent.delete()
        return redirect('/mailer')
        context = {
            'emailcontent': emailcontent
        }
        return render(request, 'mailer/delete_detail.html', context)
    else:
        return render(request, 'mailer/delete_detail.html')
