from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import MailJob, Archive
from .form import EmailForm, AttachmentForm, SignUpForm, LoginForm, DivErrorList
from win32com import client
import schedule
import time
import os


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse('index'))
    else:
        form = SignUpForm()
    context = {
        'form': form
    }
    return render(request, 'mailer/sign_up.html', context)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST, error_class=DivErrorList)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect(reverse('index'))

    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'mailer/login.html', context)


def logout_view(request):
    logout(request)
    return redirect(reverse('index'))
    return render(request, 'mailer/logout.html')


def index(request):
    if request.method == 'POST':
        form = LoginForm(request.POST, error_class=DivErrorList)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect(reverse('index'))

    else:
        form = LoginForm()
    context = {
        'form': form
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


"""
Mailjob task  
"""


def mailjob(request):
    if not request.user.is_authenticated:
        return redirect(reverse('mailer:login'))
    user_id = request.user.id
    MailJobs = MailJob.objects.filter(created_by=user_id)
    context = {
        'objects': MailJobs
    }
    return render(request, 'mailer/mailjob.html', context)


def mailjob_add(request):
    if not request.user.is_authenticated:
        return redirect(reverse('mailer:login'))

    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():

            instance = form.save(commit=False)
            created_by = User.objects.get(id=request.user.id)
            instance.created_by = created_by
            instance.save()
            form.save_m2m()

            return redirect(reverse('mailer:mailjob'))
    else:
        form = EmailForm()
    context = {
        'form': form
    }
    return render(request, 'mailer/mailjob_add.html', context)


def mailjob_edit(request, id):
    if not request.user.is_authenticated:
        return redirect(reverse('mailer:login'))

    instance = get_object_or_404(klass=MailJob, pk=id)
    user_id = request.user.id
    if instance.created_by_id == user_id:
        if request.method == 'POST':
            form = EmailForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                form.save()
                return redirect(reverse('mailer:mailjob'))
        else:
            form = EmailForm(instance=instance)
        context = {
            'form': form
        }
        return render(request, 'mailer/mailjob_edit.html', context)
    else:
        return redirect(reverse('index'))


def mailjob_delete(request, id):
    if not request.user.is_authenticated:
        return redirect(reverse('mailer:login'))

    instance = get_object_or_404(klass=MailJob, pk=id)
    user_id = request.user.id
    if instance.created_by_id == user_id:
        if request.method == 'POST':
            instance.delete()
            return redirect(reverse('index'))
        return render(request, 'mailer/mailjob_delete.html')
    else:
        return redirect(reverse('index'))


"""
Attachment 
"""


def archive(request):
    if not request.user.is_authenticated:
        return redirect(reverse('mailer:login'))

    user_id = request.user.id
    attachments = Archive.objects.filter(created_by=user_id)
    context = {
        'objects': attachments
    }
    return render(request, 'mailer/archive.html', context)


def archive_add(request):
    if not request.user.is_authenticated:
        return redirect(reverse('mailer:login'))

    if request.method == 'POST':
        form = AttachmentForm(request.POST, request.FILES)

        if form.is_valid():
            archive_name = form.cleaned_data['archive'].name
            instance = form.save(commit=False)
            instance.archive_name = archive_name
            created_by = User.objects.get(id=request.user.id)
            instance.created_by = created_by
            instance.save()
            return redirect(reverse('mailer:archive'))
    else:
        form = AttachmentForm()
    context = {
        'form': form
    }
    return render(request, 'mailer/archive_add.html', context)


def archive_delete(request, id):
    if not request.user.is_authenticated:
        return redirect(reverse('mailer:login'))

    instance = get_object_or_404(klass=Archive, pk=id)
    user_id = request.user.id
    if instance.created_by_id == user_id:
        if request.method == 'POST':
            instance.delete()
            return redirect(reverse('mailer:archive'))
        context = {
            'archive': archive
        }
        return render(request, 'mailer/archive_delete.html', context)
    else:
        return redirect(reverse('mailer:archive'))


"""
Send mail by schedule
"""


def mail_schedule(request):
    for profile in MailJob:
        if profile.status == "activate":
            def mail_job(request):
                send_mail(
                    subject=profile.subject,
                    to=profile.to,
                    body=profile.body,
                    attachments=profile.attachment
                )
            if profile.executed_on == "monday":
                schedule.every().monday.at(profile.executed_at).do(mail_job)

            elif profile.executed_on == "tuesday":
                schedule.every().tuesday.at(profile.executed_at).do(mail_job)

            elif profile.executed_on == "wednesday":
                schedule.every().wednesday.at(profile.executed_at).do(mail_job)

            elif profile.executed_on == "thursday":
                schedule.every().thursday.at(profile.executed_at).do(mail_job)

            elif profile.executed_on == "friday":
                schedule.every().friday.at(profile.executed_at).do(mail_job)
