from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.qr_scanner, name='scanner'),
<<<<<<< HEAD
    path('process_qr_scan/', views.process_qr_scan, name='qr_scan'),
    path('process_qr_scan/quantity', include('quantity.urls')),
=======
    path('process_qr_scan/', views.process_qr_scan, name='process_qr_scan'),
>>>>>>> f46439a400050389cba3f654b996178bc6a4753b
    path('add_item/', views.add_item, name='add_item'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)