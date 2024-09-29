from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView, PasswordChangeView
from qrcodes import views as qrcodes_views

urlpatterns = [
    path('', views.home, name='home'),
    path('info', views.info, name='info'),
    path('news/', views.news, name='news'),
    path('add_news/', views.add_news, name='add_news'),
    path('action_add/', include('action_add.urls')),
    path('action_take/', include('action_take.urls')),
    path('action_return/', include('action_return.urls')),
    path('action_remove/', include('action_remove.urls')),
    path('profile/', views.profile, name='profile'),
    path('profile/statistics/', views.statistics, name='statistics'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/change_password/', PasswordChangeView.as_view(), name='change_password'),
    path('add_item/', qrcodes_views.add_item, name='add_item'),
    path('add_user/', views.add_user, name='add_user'),
    path('stock/', views.stock, name='stock')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
