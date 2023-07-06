
from django.urls import path 

from .views.api_user_views import ApiUserListView, create_api_user, ApiUserDetailView, ApiUserUpdateView, activate_user
from .views.warning_views import (WarningListView, WarningDetailView, WarningCreateView,
                                   WarningUpdateView, warning_delete, WarningDiscardView,
                                   warning_assign, warning_create_incidence)
from .views.incidence_views import (IncidenceListView, IncidenceDetailView, IncidenceCreateView, IncidenceUpdateView, 
                                    incidence_delete, IncidenceManagmentView)
from .views.advice_views import AdviceListView, AdviceDetailView, AdviceCreateView, AdviceUpdateView, advice_delete
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
    path('avisos/desactivar/<str:pk>/', WarningDiscardView.as_view(), name='warning_deactivate'),
    path('avisos/asignar/<str:pk>/', warning_assign, name='warning_assign'),
    path('avisos/crear-incidencia/<str:pk>/', warning_create_incidence, name='warning_create_incidence'),
    
    
    
    #-------------------------------------------------------------------
    path('incidencias/', IncidenceListView.as_view(), name='incidence_list'),
    path('incidencias/manejo/', IncidenceManagmentView.as_view(), name='incidence_managment'),
    
    path('incidencias/crear/', IncidenceCreateView.as_view(), name='incidence_create'),
    path('incidencias/detalles/<str:pk>/', IncidenceDetailView.as_view(), name='incidence_detail'),
    path('incidencias/modificar/<str:pk>/', IncidenceUpdateView.as_view(), name='incidence_update'),
    path('incidencias/eliminar/', incidence_delete, name='incidence_delete'),
    #------------------------------------------------------------------------------------------------
    path('consejos/', AdviceListView.as_view(), name='advice_list'),
    path('consejos/crear/', AdviceCreateView.as_view(), name='advice_create'),
    
    path('consejos/detalles/<str:pk>/', AdviceDetailView.as_view(), name='advice_detail'),
    path('consejos/modificar/<str:pk>/', AdviceUpdateView.as_view(), name='advice_update'),
    path('consejos/eliminar/', advice_delete, name='advice_delete'),





]