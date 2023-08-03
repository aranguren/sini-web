import jwt
from passlib.hash import pbkdf2_sha256 as sha256
from rest_framework.authentication import BaseAuthentication
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from django.conf import settings
from sini.models import BlacklistedToken, ApiUser


class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        # Return the failure reason instead of an HttpResponse
        return reason


class SafeJWTAuthentication(BaseAuthentication):
    '''
        custom authentication class for DRF and JWT
        https://github.com/encode/django-rest-framework/blob/master/rest_framework/authentication.py
    '''

    def authenticate(self, request):

        #User = get_user_model()
        authorization_heaader = request.headers.get('Authorization')

        if not authorization_heaader:
            return None
            #raise exceptions.AuthenticationFailed("Debe proveer credenciales, token de autenticacion no encontrado", code=404)
            
        try:
            # header = 'Token xxxxxxxxxxxxxxxxxxxxxxxx'
            access_token = authorization_heaader.split(' ')[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('El token ha expirado')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')

        apiuser = ApiUser.objects.filter(id=payload['user_id']).first()
        if apiuser is None:
            raise exceptions.AuthenticationFailed('Usuario no encontrado')
        if not apiuser.active:
            raise exceptions.AuthenticationFailed('Usuario no activo')
       
        authorization = request.META.get("HTTP_AUTHORIZATION")
        token = authorization.split(" ")[1]
        is_logout = BlacklistedToken.objects.filter(token=token).first()

        if is_logout:
            raise exceptions.PermissionDenied("El token no es válido debe loguearse")
        #if not user.is_active:
        #    raise exceptions.AuthenticationFailed('user is inactive')

        #self.enforce_csrf(request)
        

        return (apiuser, token)
    
    def enforce_csrf(self, request):
        
        #Enforce CSRF validation
        
        check = CSRFCheck()
        # populates request.META['CSRF_COOKIE'], which is used in process_view()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        print(reason)
        if reason:
            # CSRF failed, bail with explicit error message
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)
    
