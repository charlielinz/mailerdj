from django.db import models

class EmailContent(models.Model):
    subject = models.CharField(max_length=200)
    body = models.CharField(max_length=200)
    to = models.CharField(max_length=200)
    attachment = models.CharField(max_length=200)
    