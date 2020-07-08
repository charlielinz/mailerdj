from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mailer/', include('mailer.urls')),
    path('', RedirectView.as_view(url='/mailer/'), name='index'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
