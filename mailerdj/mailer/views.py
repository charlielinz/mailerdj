from django.shortcuts import render
from win32com import client
import schedule
import time
import os
import json


def index(request):
    context = {
        'text': 'hello!'
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
    context = {

    }
    return render(request, 'mailer/add_detail.html', context)

def edit_detail(request):
    context = {

    }
    return render(request, 'mailer/edit_detail.html', context)

def delete_detail(request):
    context = {
        
    }
    return render(request, 'mailer/delete_detail.html', context)
