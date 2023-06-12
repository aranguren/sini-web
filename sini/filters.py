import django_filters
from .models import Incidence

class ProductFilter(django_filters.FilterSet):

    class Meta:
        model = Incidence
        fields = ['price', 'release_date', 'manufacturer']

        fields = {
                    'name': ['icontains'],
                    'descripcion': ['icontains'],
                    'tipo_incidente': ['exact'],
                    'status': ['exact'],
                }