from django.db import models

class EmailContent(models.Model):
    task_name = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    body = models.TextField(max_length=200)
    to = models.CharField(max_length=200)
    attachment = models.CharField(max_length=200)
    