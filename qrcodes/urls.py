from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.qr_scanner, name='scanner'),
    path('quantity/', include('quantity.urls')),
    path('add_item/', views.add_item, name='add_item'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)