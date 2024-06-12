from django.shortcuts import render
#from rest_framework_simplejwt.authentication import JWTAuthentication
#from rest_framework.permissions import IsAuthenticated
from .authentication import SafeJWTAuthentication
from .permissions import IsUserAuthenticated, IsUserOwner
from rest_framework import generics
from sini.models import Incidence, ApiUser, MobileWarning, Advice, IncidenceType, SiniFCMDevice
from .serializers import SiniFCMDeviceSerializer, IncidenceSerializer, WarningSerializer, UploadWarningFilesSerializer, AdviceSerializer, IncidenceTypeSerializer
from django_filters import rest_framework as filters
from .filters import IncidenceFilterDRF
import uuid
from django.contrib.auth import get_user_model
from django.core import serializers
from rest_framework import exceptions, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
#from accounts.serializers import UserSerializer
from .tokens import generate_access_token, generate_refresh_token
from passlib.hash import pbkdf2_sha256 as sha256

from rest_framework.response import Response

from rest_framework.views import APIView
import json



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

class WarningAPICreate(generics.CreateAPIView):
    authentication_classes = [SafeJWTAuthentication]
    permission_classes = (IsUserAuthenticated,)
    queryset = MobileWarning.objects.all()
    serializer_class = WarningSerializer

    def perform_create(self, serializer):
        if self.request.user.is_anonymous:
            serializer.save(creation_origin="api", active=True  )
        else:
            serializer.save(created_by_api_user=self.request.user, 
            modified_by_api_user=self.request.user,creation_origin="api", active=True  )




class WarningAPIUpdate(generics.UpdateAPIView):
    authentication_classes = [SafeJWTAuthentication]
    permission_classes = (IsUserAuthenticated,)
    queryset = MobileWarning.objects.all()
    serializer_class = UploadWarningFilesSerializer

    def perform_update(self, serializer):
        if not self.request.user.is_anonymous:
            serializer.save( modified_by_api_user=self.request.user,  )
        else:
            serializer.save()


    

class IncidenceTypeAPIRetrieve(generics.ListAPIView):
    authentication_classes = [SafeJWTAuthentication]
    permission_classes = (IsUserAuthenticated,)
    queryset = IncidenceType.objects.all()
    serializer_class = IncidenceTypeSerializer







class AdviceAPIList(generics.ListAPIView):
    authentication_classes = [SafeJWTAuthentication]
    permission_classes = (IsUserAuthenticated,)
    queryset = Advice.objects.all()
    serializer_class = AdviceSerializer


class FCMTokenView(APIView):
    authentication_classes = [SafeJWTAuthentication]
    permission_classes = (IsUserAuthenticated,)
    """
    List all snippets, or create a new snippet.
    """


    def post(self, request, format=None):
        """
        Recibe el token y el tipo de dispositivo. Si el usuario no tiene dispositivo lo crea.
        Si ya tiene actualiza la informacion del dispositivo
        """
        user = request.user

        serializer = SiniFCMDeviceSerializer(data=request.data)
        #Calling .save() will either create a new instance, or update an existing instance, depending on if an existing instance was passed when instantiating the serializer class:

        # .save() will create a new instance.
        #serializer = CommentSerializer(data=data)

        # .save() will update the existing `comment` instance.
        #serializer = CommentSerializer(comment, data=data)
        #serializer = FCMDeviceSerializer(request.data)
        if serializer.is_valid():
            registration_id = request.data.get('registration_id')
            try:
                found_device = SiniFCMDevice.objects.get(registration_id=registration_id)
            except SiniFCMDevice.DoesNotExist:
                # We have no object! Do something...
                device = serializer.save()
                device.user = user
                device_id = str(uuid.uuid4())
                device.name = f"{user.name} ({device_id})"
                device.device_id = device_id
                device.save()

                values = {
                    "name": device.name,
                    "device_id": device.device_id,
                    "registration_id": device.registration_id,
                    "type": device.type,
                    "active": device.active,
                    "created": device.created,
                    "modified": device.modified,

                }

                return Response(values, status=status.HTTP_201_CREATED)
            else:
                if found_device.user==user:
                    return Response({'detail': 'El usuario ya tiene el token asignado. Nada que hacer'}, status=status.HTTP_202_ACCEPTED)
                elif found_device.user.is_anonymous and not user.is_anonymous:
                    found_device.user = user
                    found_device.name = f"{user.name} ({found_device.device_id})"
                    found_device.save()

                    values = {
                        "name": found_device.name,
                        "device_id": found_device.device_id,
                        "registration_id": found_device.registration_id,
                        "type": found_device.type,
                        "active": found_device.active,
                        "created": found_device.created,
                        "modified": found_device.modified,

                    }

                    return Response(values, status=status.HTTP_200_OK)
                
                elif not found_device.user.is_anonymous and user.is_anonymous:
                    return Response({'detail': 'Ya existe un usuario (no anónimo) con el mismo token. No se efectuará ningún cambio'}, status=status.HTTP_202_ACCEPTED)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
