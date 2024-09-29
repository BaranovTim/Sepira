from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.return_back, name='return_back'),
    path('preaction_fifth/qrcodes/', include('qrcodes.urls')),
    path('preaction_sixth/qrcodes/', include('qrcodes.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)