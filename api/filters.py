from django_filters import rest_framework as filters
from sini.models import Incidence

class IncidenceFilterDRF(filters.FilterSet):

    name = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    incidence_type = filters.CharFilter(lookup_expr='exact')
    status = filters.CharFilter(lookup_expr='exact')



    class Meta:
        model = Incidence
        fields = ['name', 'description', 'incidence_type', 'status']
        """
        fields = {
                    'name': ['icontains',],
                    'descripcion': ['icontains',],
                    'tipo_incidente': ['exact',],
                    'status': ['exact',],
                }
        """
        