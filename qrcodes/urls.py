from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.qr_scanner, name='scanner'),
    path('process_qr_scan/', views.process_qr_scan, name='process_qr_scan'),
    path('add_item/', views.add_item, name='add_item'),
    path('quantity/', include('quantity.urls'))

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)