
from django.urls import path 

from .views.api_user_views import ApiUserListView, create_api_user, ApiUserDetailView, ApiUserUpdateView, activate_user
from .views.warning_views import WarningListView, WarningDetailView, WarningCreateView, WarningUpdateView, warning_delete

app_name = 'sini'

urlpatterns = [
    path('usuarios-moviles/', ApiUserListView.as_view(), name='api_user_list'),
    path('usuarios-moviles/crear/', create_api_user, name='api_user_create'),
    path('usuarios-moviles/detalles/<str:pk>/', ApiUserDetailView.as_view(), name='api_user_detail'),
    path('usuarios-moviles/modificar/<str:pk>/', ApiUserUpdateView.as_view(), name='api_user_update'),
    #path('finca/listado', FarmListView.as_view(),name='farm_list'),

    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  
        activate_user, name='activate_user'),  

    #-----------------------------------------------------------------
    path('avisos/', WarningListView.as_view(), name='warning_list'),
    path('avisos/crear/', WarningCreateView.as_view(), name='warning_create'),
    path('avisos/detalles/<str:pk>/', WarningDetailView.as_view(), name='warning_detail'),
    path('avisos/modificar/<str:pk>/', WarningUpdateView.as_view(), name='warning_update'),
    path('avisos/eliminar/', warning_delete, name='warning_delete'),


]