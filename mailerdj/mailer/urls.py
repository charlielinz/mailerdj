from django.urls import path
from .views import index, mailjob, mailjob_add, mailjob_edit, mailjob_delete, archive, archive_add, archive_delete, sign_up, login_view, logout_view

app_name = 'mailer'
urlpatterns = [
    path('', index, name='index'),
    path('mailjob', mailjob, name='mailjob'),
    path('mailjob_add/', mailjob_add, name='mailjob_add'),
    path('mailjob_edit/<int:id>', mailjob_edit, name='mailjob_edit'),
    path('mailjob_delete/<int:id>/', mailjob_delete, name='mailjob_delete'),
    path('archive/', archive, name='archive'),
    path('archive_add/', archive_add, name='archive_add'),
    path('archive_delete/<int:id>/', archive_delete, name='archive_delete'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('sign_up/', sign_up, name='sign_up')
]
