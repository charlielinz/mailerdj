from django.db import models
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
import os
import uuid


class MyFileSystemStorage(FileSystemStorage):

    def generate_filename(self, filename):
        dirname, filename = os.path.split(filename)
        new_filename = str(uuid.uuid4()) + os.path.splitext(filename)[1]
        return os.path.normpath(os.path.join(dirname, new_filename))


mfss = MyFileSystemStorage()


class MailJob(models.Model):
    task_name = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    body = models.TextField(max_length=1000)
    to = models.CharField(max_length=200)
    attachment = models.ManyToManyField(to='Archive')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)


class Archive(models.Model):
    archive = models.FileField(storage=mfss, upload_to='mailer/archive')
    archive_name = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.archive_name
