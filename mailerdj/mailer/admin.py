from django.contrib import admin
from .models import MailJob
from .models import Archive

admin.site.register(MailJob)
admin.site.register(Archive)
