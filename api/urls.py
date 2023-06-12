from django.views.decorators.cache import cache_page
from django.urls import path 

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import IncidenceAPIList, IncidenceAPICreate
app_name = 'api'

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('incidencias/', IncidenceAPIList.as_view()),
    path('incidencias/crear/', IncidenceAPICreate.as_view()),
    #path('finca/listado', FarmListView.as_view(),name='farm_list'),
    #path('finca/detalles/<str:pk>', FarmDetailView.as_view(),name='farm_detail'),

    
]