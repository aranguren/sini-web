from django.views.decorators.cache import cache_page
from django.urls import path 

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import IncidenceAPIList, IncidenceAPICreate, IncidenceAPIRetrieve
app_name = 'api'

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('incidencias/', IncidenceAPIList.as_view(), 'incidence_list'),
    path('incidencias/crear/', IncidenceAPICreate.as_view(), 'incidence_create'),
    #path('finca/listado', FarmListView.as_view(),name='farm_list'),
    path('incidencias/detalles/<str:pk>/', IncidenceAPIRetrieve.as_view(),name='incidence_detail'),


    

    
]