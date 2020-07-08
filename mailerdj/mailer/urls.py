from django.urls import path
from .views import index, mailjob_add, mailjob_edit, mailjob_delete, archive, archive_add, archive_delete

app_name = 'mailer'
urlpatterns = [
    path('', index, name='index'),
    path('mailjob_add/', mailjob_add, name='mailjob_add'),
    path('mailjob_edit/<int:id>', mailjob_edit, name='mailjob_edit'),
    path('mailjob_delete/<int:id>/', mailjob_delete, name='mailjob_delete'),
    path('archive/', archive, name='archive'),
    path('archive_add/', archive_add, name='archive_add'),
    path('archive_delete/<int:id>/', archive_delete, name='archive_delete'),
]
