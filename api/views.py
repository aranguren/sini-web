from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from sini.models import Incidence
from .serializers import IncidenceSerializer
from django_filters import rest_framework as filters
from .filters import IncidenceFilterDRF

from django.contrib.auth import get_user_model

from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
#from accounts.serializers import UserSerializer
from .tokens import generate_access_token, generate_refresh_token
from passlib.hash import pbkdf2_sha256 as sha256
from sini.models import ApiUser
from rest_framework.response import Response




@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def login_view(request):


    user_email = request.data.get('email')
    password = request.data.get('password')
    response = Response()
    if (user_email is None) or (password is None):
        raise exceptions.AuthenticationFailed(
            'User email and password required')

    user = ApiUser.objects.filter(email=user_email).first()

    if(user is None):
        raise exceptions.AuthenticationFailed('Wrong user or password')
    try:
        if (not user.check_password(password)):
            raise exceptions.AuthenticationFailed('Wrong user or password')
    except ValueError:
        raise exceptions.NotAcceptable("El usuario no ha establecido contrasenha hash")
    #serialized_user = UserSerializer(user).data

    if not user.active:
        raise exceptions.AuthenticationFailed('User is not active')


    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
    response.data = {
        'access_token': access_token,
        'refresh_token': refresh_token,
    }

    return response


class IncidenceAPIList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    queryset = Incidence.objects.all()
    serializer_class = IncidenceSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IncidenceFilterDRF


class IncidenceAPIRetrieve(generics.RetrieveAPIView):
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