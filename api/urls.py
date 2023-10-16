from django.views.decorators.cache import cache_page
from django.urls import path 

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (login_view, WarningAPICreate, WarningAPIUpdate, AdviceAPIList,
                    FCMTokenView, IncidenceTypeAPIRetrieve)
app_name = 'api'

urlpatterns = [
    
    path('login/', login_view, name='login'),
    #path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('avisos/crear/', WarningAPICreate.as_view(), name='warning_create'),
    path('avisos/subir-archivos/<str:pk>/', WarningAPIUpdate.as_view(), name='warning_upload_files'),
    path('consejos/', AdviceAPIList.as_view(), name='advice_list'),
    path('tipos-incidencias/', IncidenceTypeAPIRetrieve.as_view(), name='incidence_type_list'),

    

    path('token/crear/', FCMTokenView.as_view(),name='token_import'),

    

    
]