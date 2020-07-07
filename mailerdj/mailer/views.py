from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import EmailContent, Library
from .form import EmailForm, AttachmentForm
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
        form = EmailForm(request.POST, request.FILES)

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
        form = EmailForm(request.POST, request.FILES, instance=instance)
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
        return redirect('/mailer/')
        context = {
            'emailcontent': emailcontent
        }
        return render(request, 'mailer/delete_detail.html', context)
    else:
        return render(request, 'mailer/delete_detail.html')


def get_file_name(file_path):
    index = []
    n = 0
    for letter in file_path:
        if letter == '/':
            index.append(n)
        n += 1
    max_index = index[-1]
    file_name = file_path[(max_index+1):-1]
    return file_name


def library(request):
    attachments = Library.objects.all()
    for attachment in attachments:
        attachment.file_name = get_file_name(attachment.book.name)
        attachment.save()
    context = {
        'objects': attachments
    }
    return render(request, 'mailer/library.html', context)


def add_new_file(request):
    if request.method == 'POST':
        form = AttachmentForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('/mailer/library/')
        context = {
            'form': form
        }
        return render(request, 'mailer/add_new_file.html', context)
    else:
        form = AttachmentForm()
        context = {
            'form': form
        }
        return render(request, 'mailer/add_new_file.html', context)


def delete_file(request, id):
    if request.method == 'POST':
        try:
            library = Library.objects.get(id=id)
        except Library.DoesNotExist:
            raise Http404('Page do not exist')
        library.delete()
        return redirect('/mailer/library/')
        context = {
            'library': library
        }
        return render(request, 'mailer/delete_file.html', context)
    else:
        return render(request, 'mailer/delete_file.html')
