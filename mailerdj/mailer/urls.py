from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import index, add_detail, edit_detail, delete_detail

app_name = 'mailer'
urlpatterns = [
    path('', index, name='index'),
    path('add_detail/', add_detail, name='add_detail'),
    path('edit_detail/<int:id>', edit_detail, name='edit_detail'),
    path('delete_detail/<int:id>/', delete_detail, name='delete_detail')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
