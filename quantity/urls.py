from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.quantity, name='quantity'),
    path('/download/csv/', views.download_qrscans_csv, name='download_qrscans_csv')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
