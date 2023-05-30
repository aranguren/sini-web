from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from django.conf import settings

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

class Incidencia(BasicAuditModel):

    TIPO_INCIDENTES_CHOICES = (
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
    geom = models.PointField(verbose_name=_("Localización"), srid=4326, blank=True, null=True)

    name = models.CharField(_("Nombre"), max_length=255)
    tipo_incidente = models.CharField(_("Tipo incidente"), max_length=50, choices=TIPO_INCIDENTES_CHOICES, default="tipo1")
    descripcion = models.TextField(_("Descripción"), blank=True, null=True)
    
    status = models.CharField(_("Status"), max_length=50, choices=STATUS_CHOICES, default="creado")
    
    foto1 = models.FileField(verbose_name=_("Foto 1"), upload_to="incidencia_fotos",
                                                null=False, blank=False)
    foto2 = models.FileField(verbose_name=_("Foto 2"), upload_to="incidencia_fotos",
                                                null=False, blank=False)
    foto3 = models.FileField(verbose_name=_("Foto 3"), upload_to="incidencia_fotos",
                                                null=False, blank=False)
    audio = models.FileField(verbose_name=_("Audio"), upload_to="incidencia_audioa",
                                                null=False, blank=False)
    
    video = models.FileField(verbose_name=_("Video"), upload_to="incidencia_video",
                                                null=False, blank=False)

    

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sini_incidencia'
        managed = True
        verbose_name =  'Incidencia'
        verbose_name_plural =  'Incidencias'
