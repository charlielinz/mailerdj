from django.contrib import admin
from .models import EmailContent
from .models import Library

admin.site.register(EmailContent)
admin.site.register(Library)
