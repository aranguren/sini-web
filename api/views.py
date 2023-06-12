from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from sini.models import Incidence
from .serializers import IncidenceSerializer
from django_filters import rest_framework as filters
from .filters import IncidenceFilterDRF




class IncidenceAPIList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    queryset = Incidence.objects.all()
    serializer_class = IncidenceSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IncidenceFilterDRF

    """
    def get_queryset(self):

        if self.request.user.is_superuser:
            query_result =  Incidencia.objects.order_by('name')
        else:
            query_result =  Incidencia.objects.filter(created_by__id=self.request.user.id).order_by('name')

        query = {'name': self.request.query_params.get('name', None),
                 'codigo': self.request.query_params.get('codigo', None)}


        if query['name'] and query['name'] != '':
            query_result = query_result.filter(name__icontains=query['name'])
        if query['codigo'] and query['codigo'] != '':
            query_result = query_result.filter(codigo__icontains=query['codigo'])
        return query_result
    """


class IncidenceAPICreate(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    queryset = Incidence.objects.all()
    serializer_class = IncidenceSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, 
        modified_by=self.request.user,  )

"""
class FarmAPIUpdate(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    queryset = FarmModel.objects.all()
    serializer_class = FarmWriteSerializer



    def put(self, request, *args, **kwargs):
        farm = self.get_object()
        if self.request.user.is_superuser:
            print("User has permisions")
        elif self.request.user.id != farm.created_by.id:
            raise PermissionDenied()

        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        farm = self.get_object()
        if self.request.user.is_superuser:
            print("User has permisions")
        elif self.request.user.id != farm.created_by.id:
            raise PermissionDenied()
            
        return self.partial_update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save( modified_by=self.request.user,  )

class FarmAPIDelete(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    queryset = FarmModel.objects.all()
    serializer_class = FarmWriteSerializer

    def delete(self, request, *args, **kwargs):
        farm = self.get_object()
        if self.request.user.is_superuser:
            print("User has permisions")
        elif self.request.user.id != farm.created_by.id:
            raise PermissionDenied()

        return self.destroy(request, *args, **kwargs)

"""