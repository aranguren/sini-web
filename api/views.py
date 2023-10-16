from django.shortcuts import render
#from rest_framework_simplejwt.authentication import JWTAuthentication
#from rest_framework.permissions import IsAuthenticated
from .authentication import SafeJWTAuthentication
from .permissions import IsUserAuthenticated, IsUserOwner
from rest_framework import generics
from sini.models import Incidence, ApiUser, MobileWarning, Advice, IncidenceType
from .serializers import FCMDeviceSerializer, IncidenceSerializer, WarningSerializer, UploadWarningFilesSerializer, AdviceSerializer, IncidenceTypeSerializer
from django_filters import rest_framework as filters
from .filters import IncidenceFilterDRF

from django.contrib.auth import get_user_model

from rest_framework import exceptions, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
#from accounts.serializers import UserSerializer
from .tokens import generate_access_token, generate_refresh_token
from passlib.hash import pbkdf2_sha256 as sha256

from rest_framework.response import Response

from fcm_django.models import FCMDevice
from rest_framework.views import APIView




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
        if user.device:
            created=False
            serializer = FCMDeviceSerializer(user.device, data=request.data)
        else:
            created=True
            serializer = FCMDeviceSerializer(data=request.data)
        #Calling .save() will either create a new instance, or update an existing instance, depending on if an existing instance was passed when instantiating the serializer class:

        # .save() will create a new instance.
        #serializer = CommentSerializer(data=data)

        # .save() will update the existing `comment` instance.
        #serializer = CommentSerializer(comment, data=data)
        #serializer = FCMDeviceSerializer(request.data)
        if serializer.is_valid():
            device = serializer.save()
            if created:
                device.name = f"{user.name}({user.email})"
                user.device = device
                user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
