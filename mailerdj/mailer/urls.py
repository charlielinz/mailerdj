from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import index, add_detail, edit_detail, delete_detail, library, add_new_file, delete_file

app_name = 'mailer'
urlpatterns = [
    path('', index, name='index'),
    path('add_detail/', add_detail, name='add_detail'),
    path('edit_detail/<int:id>', edit_detail, name='edit_detail'),
    path('delete_detail/<int:id>/', delete_detail, name='delete_detail'),
    path('library/', library, name='library'),
    path('add_new_file/', add_new_file, name='add_new_file'),
    path('delete_file/<int:id>/', delete_file, name='delete_file'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
