from django.db import models

class EmailContent(models.Model):
    task_name = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    body = models.TextField(max_length=1000)
    to = models.CharField(max_length=200)
    attachment = models.ManyToManyField(to='Library')
    

class Library(models.Model):
    book = models.FileField(upload_to='library')
    file_name = models.CharField(max_length=200)
    def __str__(self):
        return self.file_name
