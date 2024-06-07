from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from passlib.hash import pbkdf2_sha256 as sha256
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import post_save
from django.dispatch import receiver
# requeridos para enviar mensajes
from firebase_admin.messaging import Message
from computedfields.models import ComputedFieldsModel, computed, compute
from .validators import validate_audio_file_extension, validate_video_file_extension
import datetime

from firebase_admin import messaging
from firebase_admin.messaging import Message
# Create your models here.

class BasicAuditModel(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, 
                related_name="+",
                verbose_name=_("Creado por"), 
                null=True,
                blank=False,
                on_delete=models.SET_NULL)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, 
                    related_name="+",
                    verbose_name=_("Modificado por"), 
                    null=True,
                    blank=False,
                    on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha creado"))
    modified = models.DateTimeField(auto_now=True, verbose_name=_("Fecha modificado"))


    class Meta:
        abstract = True

class Incidence(BasicAuditModel, ComputedFieldsModel):

    INCIDENCE_TYPE_CHOICES = (
        ("accidente_aereo", "Accidente aéreo"),
        ("accidente_transito", "Accidente de tránsito"),
        ("colapso_puente", "Alerta por colapso de puente"),
        ("arbol_caido", "Árbo caído"),
        ("asfixia_inmersion", "Asfixia por inmersión"),
        ("aumento_cauce", "Aumento de cauce"),
        ("aumento_caudal", "Aumento  de caudal")
    )
    STATUS_CHOICES = (
        ("creado","Creado"),
        ("finalizado","Finalizado"),
    )
    


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    active = models.BooleanField(_("Activo?"), default=True)

    geom = models.PointField(verbose_name=_("Localización"), srid=4326, blank=False, null=False)

    name = models.CharField(_("Nombre"), max_length=255)
    #type_incidence = models.CharField(_("Tipo incidente"), max_length=50, choices=INCIDENCE_TYPE_CHOICES, default="tipo1")
    type_incidence = models.ForeignKey("IncidenceType", verbose_name=_("Tipo incidente"), on_delete=models.RESTRICT)
    @computed(models.CharField(_("Tipo incidente"), max_length=255),
                                depends=[('type_incidence', ['name'])])
    def type_incidence_str(self):

        if self.type_incidence:
            return self.type_incidence.name
        else:
            return ""
        
    description = models.TextField(_("Descripción"), blank=True, null=True)
    
    status = models.CharField(_("Status"), max_length=50, choices=STATUS_CHOICES, default="creado")
    
    image1 = models.ImageField(verbose_name=_("Foto 1"), upload_to="incidencia_fotos",
                                                null=True, blank=True)
    image2 = models.ImageField(verbose_name=_("Foto 2"), upload_to="incidencia_fotos",
                                                null=True, blank=True)
    image3 = models.ImageField(verbose_name=_("Foto 3"), upload_to="incidencia_fotos",
                                                null=True, blank=True)
    audio = models.FileField(verbose_name=_("Audio"), upload_to="incidencia_audioa", 
                                                validators=[validate_audio_file_extension],
                                                null=True, blank=True)
    
    video = models.FileField(verbose_name=_("Video"), upload_to="incidencia_video",
                                                validators=[validate_video_file_extension],
                                                null=True, blank=True)    

    priority = models.IntegerField(_("Prioridad"), default=1, 
                                   validators=[MaxValueValidator(5), MinValueValidator(1)])
    def __str__(self):
        return self.name
    
    def get_warnings(self):
        return self.mobile_warnings.all()

    class Meta:
        db_table = 'sini_incidence'
        managed = True
        ordering = ["-created"]
        verbose_name =  'Incidencia'
        verbose_name_plural =  'Incidencias'



class MobileWarning(BasicAuditModel, ComputedFieldsModel):

    INCIDENCE_TYPE_CHOICES = (
        ("accidente_aereo", "Accidente aéreo"),
        ("accidente_transito", "Accidente de tránsito"),
        ("colapso_puente", "Alerta por colapso de puente"),
        ("arbol_caido", "Árbo caído"),
        ("asfixia_inmersion", "Asfixia por inmersión"),
        ("aumento_cauce", "Aumento de cauce"),
        ("aumento_caudal", "Aumento  de caudal")
    )
    STATUS_CHOICES = (
        ("creado","Creado"),
        ("asignado","Asignado"),
        ("descartado","Descartado"),
    )
    CREATION_CHOICES = (
        ("api","API"),
        ("web","WEB"),
    )
    


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    active = models.BooleanField(_("Activo?"), default=True)
    geom = models.PointField(verbose_name=_("Localización"), srid=4326, blank=False, null=False)

    name = models.CharField(_("Nombre"), max_length=255)
    #type_incidence = models.CharField(_("Tipo incidente"), max_length=50, choices=INCIDENCE_TYPE_CHOICES, default="tipo1")
    type_incidence = models.ForeignKey("IncidenceType", verbose_name=_("Tipo incidente"), on_delete=models.RESTRICT)

    @computed(models.CharField(_("Tipo incidente"), max_length=255),
                                depends=[('type_incidence', ['name'])])
    def type_incidence_str(self):

        if self.type_incidence:
            return self.type_incidence.name
        else:
            return ""
    
    description = models.TextField(_("Descripción"), blank=True, null=True)
    
    status = models.CharField(_("Status"), max_length=50, choices=STATUS_CHOICES, default="creado")
    
    image1 = models.ImageField(verbose_name=_("Foto 1"), upload_to="aviso_fotos",
                                                null=True, blank=True)
    image2 = models.ImageField(verbose_name=_("Foto 2"), upload_to="aviso_fotos",
                                                null=True, blank=True)
    image3 = models.ImageField(verbose_name=_("Foto 3"), upload_to="aviso_fotos",
                                                 null=True, blank=True)
    audio = models.FileField(verbose_name=_("Audio"), upload_to="aviso_audios", 
                                               validators=[validate_audio_file_extension],
                                               null=True, blank=True)
    
    video = models.FileField(verbose_name=_("Video"), upload_to="aviso_video",
                                                validators=[validate_video_file_extension],
                                               null=True, blank=True)

    assign_incidence = models.ForeignKey("sini.Incidence", verbose_name=_("Incidencia asignada"), 
                      null=True, blank=True, related_name="mobile_warnings", 
                      on_delete=models.RESTRICT)

    creation_origin = models.CharField(_("Creado desde"), max_length=50, choices=CREATION_CHOICES, default="api")
    created_by_api_user = models.ForeignKey("ApiUser", 
                related_name="+",
                verbose_name=_("Creado por (Usuario Móvil)"), 
                null=True,
                blank=False,
                on_delete=models.RESTRICT)
    modified_by_api_user = models.ForeignKey("ApiUser", 
                    related_name="+",
                    verbose_name=_("Modificado por (Usuario Móvil)"), 
                    null=True,
                    blank=False,
                    on_delete=models.RESTRICT)
    

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sini_warning'
        managed = True
        ordering = ["-created"]
        verbose_name =  'Aviso'
        verbose_name_plural =  'Avisos'


class Advice(BasicAuditModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    name = models.CharField(_("Nombre"), max_length=254)
    description = models.TextField(_("Descripción"))
    advice = RichTextUploadingField(_("Consejo"))

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sini_advice'
        managed = True
        verbose_name = 'Consejo'
        verbose_name_plural = 'Consejos'



class ApiUser(BasicAuditModel):


    name = models.CharField(_("Nombre y apellidos"), max_length=254)
    email = models.EmailField(_("Email"), max_length=254, unique=True)

    
    password = models.CharField(max_length=250, default="usuario", blank=True, null=True)
    password_str = models.CharField(_("Password STR"), max_length=50, blank=True, null=True)
    active = models.BooleanField(_("Activo?"), default=False)

    group = models.ForeignKey("ApiGroup", verbose_name=_("Grupo"), on_delete=models.RESTRICT, related_name="usuarios")

    is_anonymous =  models.BooleanField(_("Es anónimo?"), default=False)

    def check_password(self,password):
        return sha256.verify(password, self.password)

    def set_password(self, password):
        self.password = sha256.hash(password)
        self.save()
         

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        db_table = 'sini_api_user'
        managed = True
        verbose_name = 'Usuario API'
        verbose_name_plural = 'Usuarios API'


class ApiGroup(models.Model):

    name = models.CharField(_("Nombre grupo"), max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sini_api_group'
        managed = True
        verbose_name = 'Grupos API'
        verbose_name_plural = 'Grupos API'


class BlacklistedToken(models.Model):
    
    token =  models.TextField( verbose_name="Token")
    blacklisted_date = models.DateTimeField(verbose_name=_("Fecha"), auto_now_add=True)


    def __str__(self):
        return self.token

    class Meta:
        db_table = 'sini_api_blacklisted_token'
        managed = True
        verbose_name = 'Token'
        verbose_name_plural = 'Token'

class Notification(BasicAuditModel):

    SENDTO_CHOICES = (
        ("todos","Todos"),
        ("grupo","Grupo"),
        ("uno","Uno"),
    )
    STATUS_CHOICES = (
        ("enviado","Enviado"),
        ("fallido","Fallido"),
        ("enviado_parcialmente","Enviado (Parcialmente)"),
    )

    send_to = models.CharField(_("Enviar a"), max_length=254, choices=SENDTO_CHOICES, 
                               blank=False, null=False, default='todos' )
    subject = models.CharField(_("Asunto"), max_length=254)
    message = models.TextField(_("Mensaje"))

    url_noticia = models.URLField(_("URL noticia"))
    url_imagen = models.URLField(_("URL imagen"))

    geom = models.PolygonField(verbose_name=_("Localización"), srid=4326, blank=True, null=True)
    api_user =  models.ForeignKey('ApiUser', verbose_name=_("Usuario"), related_name='notifications', on_delete=models.CASCADE, blank=True, null=True)
    api_group =  models.ForeignKey('ApiGroup',verbose_name=_("Grupo"), related_name='notifications', on_delete=models.CASCADE, blank=True, null=True)

    status = models.CharField(_("Status"), max_length=50, blank=True, null=True, choices=STATUS_CHOICES)
    status_description  = models.TextField(_("Descripción"), blank=True, null=True)
    def __str__(self):
        return self.subject

    class Meta:
        db_table = 'sini_notificacion'
        managed = True
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'

class Contact(BasicAuditModel):

    name = models.CharField(_("Nombre"), max_length=255)
    email = models.EmailField(_("Email"))
    description = models.TextField(_("Descripción"), blank=True, null=True)
    phone = models.CharField(_("Teléfono"), max_length=50, blank=True, null=True)
    address = models.CharField(_("Dirección"), max_length=255, blank=True, null=True)


    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        db_table = 'sini_contact'
        managed = True
        ordering= ["name"]
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'

class IncidenceType(BasicAuditModel):
    
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    name = models.CharField(_("Nombre"), max_length=255, unique=True)


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sini_type_incidence'
        managed = True
        ordering= ["name"]
        verbose_name = 'Tipo Incidencia'
        verbose_name_plural = 'Tipos Incidencia'

from pyfcm import FCMNotification

@receiver(post_save, sender=Notification)
def created_notification_send_push(sender, instance, created,  **kwargs):
    if created:
        data={
                "subject" : instance.subject,
                "body" : instance.message,
                "url_noticia" : instance.url_noticia,
                "url_imagen": instance.url_imagen,
            }
        if instance.geom:
            data['geom'] = instance.geom.wkt
        # mensaje = messaging.Message(data)
        if instance.send_to=='uno':
            devices = SiniFCMDevice.objects.filter(user=instance.api_user, active=True)
            if devices:
                for device in devices:
                    message = messaging.Message(
                            data,
                            android=messaging.AndroidConfig(
                                    ttl=datetime.timedelta(seconds=3600),
                                    priority='normal',
                                    notification=messaging.AndroidNotification(
                                    title=instance.subject,
                                    body=instance.message,
                                    icon='stock_ticker_update',
                                    color='#f45342',
                                    image= instance.url_imagen, #'https://firebasestorage.googleapis.com/v0/b/sini-1529613608740.appspot.com/o/FCMImages%2Fphoto1685036012.jpeg?alt=media&token=4b32205b-5e05-482c-bd08-eaa587146cf9',
                                    ),

                            ),
                            token=device.registration_id,
                    )
                    #print(message)
                    try:
                        response = messaging.send(message)
                        print('Successfully sent message:')
                        print(device.registration_id)
                    except Exception as e:
                        instance.status='fallido'
                        instance.status_description=str(e)
                        instance.save()
                    else:
                        instance.status='enviado'

            else:
                instance.status='fallido'
                instance.status_description='El usuario seleccionado no tiene dispositivos asignados o el dispositivo no está activo'
                instance.save()
        elif instance.send_to =='grupo':
            grupo = instance.api_group
            usuarios = ApiUser.objects.filter(group=grupo, active=True)
            texto=""
            fallidos=False
            devices = SiniFCMDevice.objects.filter(user__group=grupo, user_device__user__active=True, active=True)
            if(devices and len(devices)>0):
                for device in devices:
                    message = messaging.Message(
                            data,
                            android=messaging.AndroidConfig(
                                    ttl=datetime.timedelta(seconds=3600),
                                    priority='normal',
                                    notification=messaging.AndroidNotification(
                                    title=instance.subject,
                                    body=instance.message,
                                    icon='stock_ticker_update',
                                    color='#f45342',
                                    image= instance.url_imagen, #'https://firebasestorage.googleapis.com/v0/b/sini-1529613608740.appspot.com/o/FCMImages%2Fphoto1685036012.jpeg?alt=media&token=4b32205b-5e05-482c-bd08-eaa587146cf9',
                                    ),

                            ),
                            token=device.registration_id,
                    )
                    #print(message)
                    try:
                        response = messaging.send(message)
                        print('Successfully sent message:')
                        print(device.registration_id)
                    except Exception as e:
                        instance.status='fallido'
                        instance.status_description=str(e)
                        instance.save()
                    else:
                        instance.status='enviado'
            else:
                instance.status='fallido'
                instance.status_description='No existen usuarios activos en el grupo que cuenten con dispositivos'
            
            instance.save()

        elif instance.send_to=='todos':
            #print("Pasando por sendto")
            usuarios = ApiUser.objects.filter(active=True)
            texto=""
            fallidos=False
            #devices = FCMDevice.objects.filter(api_user__active=True, active=True)
            devices = SiniFCMDevice.objects.filter(active=True) # Modified by AA
            if(devices and len(devices)>0):
                for device in devices:
                    message = messaging.Message(
                            data,
                            android=messaging.AndroidConfig(
                                    ttl=datetime.timedelta(seconds=3600),
                                    priority='normal',
                                    notification=messaging.AndroidNotification(
                                    title=instance.subject,
                                    body=instance.message,
                                    icon='stock_ticker_update',
                                    color='#f45342',
                                    image= instance.url_imagen, #'https://firebasestorage.googleapis.com/v0/b/sini-1529613608740.appspot.com/o/FCMImages%2Fphoto1685036012.jpeg?alt=media&token=4b32205b-5e05-482c-bd08-eaa587146cf9',
                                    ),

                            ),
                            token=device.registration_id,
                    )
                    #print(message)
                    try:
                        response = messaging.send(message)
                        print('Successfully sent message:')
                        print(device.registration_id)
                    except Exception as e:
                        instance.status='fallido'
                        instance.status_description=str(e)
                        instance.save()
                    else:
                        instance.status='enviado'

                else:
                    instance.status='enviado'

                    for usuario in usuarios:
                        if not usuario.device or (usuario.device and not usuario.device.active):
                            texto+=f"El usuario '{usuario.name}' no tiene dispositivos activos\n"
                            fallidos=True
                    if fallidos:
                        instance.status="enviado_parcialmente"
                        instance.status_description=texto
            else:

                instance.status='fallido'
                instance.status_description='No existen usuarios activos que cuenten con dispositivos'
            

        # procedemos a enviar la notificacion mediante FCM
  

  

class DeviceType(models.TextChoices):
    IOS = "ios", "ios"
    ANDROID = "android", "android"
    WEB = "web", "web"


class SiniFCMDevice(models.Model):
    name = models.CharField(verbose_name=_("Nombre dispositivo"), max_length=255)
    device_id = models.CharField(
        verbose_name=_("Device ID"),
        blank=True,
        null=True,
        db_index=True,
        help_text=_("Identificador del dispositivo"),
        max_length=255,
    )
    registration_id = models.TextField(
        verbose_name=_("Token FCM"),
        unique=True,
    )
    type = models.CharField(choices=DeviceType.choices, max_length=10)

    active = models.BooleanField(
        verbose_name=_("Is active"),
        default=True,
        help_text=_("Los dispositivos inactivos no recibiran notificaciones"),
    )
    user = models.ForeignKey(
        "ApiUser",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="fcm_devices",
    )

    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha creado"))
    modified = models.DateTimeField(auto_now=True, verbose_name=_("Fecha modificado"))

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'sini_fcm_device'
        managed = True
        verbose_name = 'Dispositivo'
        verbose_name_plural = 'Dispositivos'