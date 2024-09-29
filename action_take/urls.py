from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.take, name='take'),
    path('preaction_seventh/qrcodes/', include('qrcodes.urls')),
    path('preaction_eighth/qrcodes/', include('qrcodes.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)