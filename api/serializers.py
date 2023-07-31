from rest_framework import generics, serializers
from rest_framework.fields import CharField
from  sini.models import Incidence, MobileWarning, Advice
from rest_framework_gis.serializers import GeoFeatureModelSerializer
#from django.contrib.auth.models import User
#from django.conf import settings#
from fcm_django.models import FCMDevice



#---------------------------------------------------------
#---------- Incidencia ----------------------------------
#----------------------------------------------------------


class IncidenceSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Incidence
        geo_field = "geom"
        fields = ('id','geom','name','incidence_type',
        'description','status', 'image1', 'image2', 'image3', 'audio', 'video')
        extra_kwargs = {'geom': {'required': True}} 
        read_only_fields = ['id','created_by', 'modified_by', 'created','modified']



class UploadWarningFilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = MobileWarning
        fields = ('image1', 'image2', 'image3', 'audio', 'video')
        #read_only_fields = ['id','created_by', 'modified_by', 'created','modified', 'created_by_api_user', 'modified_by_api_user']


class WarningSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = MobileWarning
        geo_field = "geom"
        fields = ('id','geom','name','incidence_type',
        'description',)
        extra_kwargs = {'geom': {'required': True}} 
        read_only_fields = ['id','created_by', 'modified_by', 'created','modified', 'created_by_api_user', 'modified_by_api_user', 'active']

"""
class PeriodSerializer(serializers.ModelSerializer):
    resultados_totales = TotalResultSerializer(read_only=True)
    alimentos = PeriodFoodSerializer(many=True,read_only=True)
    class Meta:
        model = PeriodModel
        fields = ['id', 'name', 'finca',
        # Número promedio de animales en el año
        'vacas_promedio_qty','novillas_promedio_qty',
        'novillos_promedio_qty','toros_promedio_qty', 
        'terneras_promedio_qty','terneros_promedio_qty',
        # Mortalidad de animales en el año
        'vacas_mortalidad_qty','novillas_mortalidad_qty',
        'novillos_mortalidad_qty','toros_mortalidad_qty', 
        'terneras_mortalidad_qty','terneros_mortalidad_qty',
        # Número de animales vendidos en el año
        'vacas_vendida_qty','novillas_vendida_qty',
        'novillos_vendida_qty','toros_vendida_qty', 
        'terneras_vendida_qty','terneros_vendida_qty',
        # Animales totales anual
        'vacas_total_anual','novillas_total_anual',
        'novillos_total_anual','toros_total_anual',
        'terneras_total_anual','terneros_total_anual',
        # Peso promedio de animales en kg
        'peso_vacas','peso_novillas_sacrificio',
        'peso_toros','peso_novillos_sacrificio', 
        'peso_terneras','peso_terneros',
        'peso_terneras_sacrificio','peso_terneros_sacrificio',
        # Parámetros Reproductivos
        'vacas_paridas_qty','edad_primer_parto',
        'vacas_pre_qty','novillas_pre_qty','reemplazo_hembras',
        'tasa_fertilidad',
        # Parámetros Productivos
        'promedio_vo', 
        'produccion_leche_dia','produccion_leche_litro_animal_dia','periodo_lactancia',
        'porciento_grasa_leche','porciento_proteina_leche',
        # Manejo de Estiércol (%)
        'excretas_corral','almacenamiento_solido',
        'compotaje','biodigestor', 
        'dispersion_diaria_seco','exceta_laguna',
        'exceta_fango','incineracion',
        'excretas_sin_manejo',
        # Total alimentos
        'total_alimentos_vacas', 'total_alimentos_otros',
        # Resultados
        'resultados_totales',
        'alimentos',
        ]     

        extra_kwargs = {
        'security_question': {'read_only': True},
        'vacas_total_anual': {'read_only': True},
        'novillas_total_anual': {'read_only': True}, 
        'novillos_total_anual': {'read_only': True},
        'toros_total_anual': {'read_only': True},
        'terneras_total_anual': {'read_only': True},
        'terneros_total_anual': {'read_only': True}, 
        'salida_mortalidad_terneras': {'read_only': True},
        'salida_mortalidad_terneros': {'read_only': True},
        'salida_mortalidad_adultos': {'read_only': True},
        'reemplazo_hembras': {'read_only': True},
        'tasa_fertilidad': {'read_only': True},
        'produccion_leche_litro_animal_dia': {'read_only': True},
        'total_alimentos_vacas': {'read_only': True},
        'total_alimentos_otros': {'read_only': True},
        'peso_novillas': {'read_only': True},
        'peso_novillos': {'read_only': True}
        }

 




"""


class AdviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Advice
        fields = ('id','name','description','advice')
        read_only_fields = ['id','created_by', 'modified_by', 'created','modified']

DEVICE_TYPE_CHOICES = (
    ("ios", "ios"),
    ("android", "android"),
    ("web", "web")
)
class FCMDeviceSerializer(serializers.Serializer):
    #device_id max_length=255,blank=True,null=True, verbose_name=_("Device ID"),
    # name -> max_length=255, verbose_name=_("Name"), blank=True, null=True
    #date_created
    registration_id = serializers.CharField()
    type = serializers.ChoiceField(choices=DEVICE_TYPE_CHOICES)

    def create(self, validated_data):
        return FCMDevice.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.registration_id = validated_data.get('registration_id', instance.registration_id)
        instance.type = validated_data.get('type', instance.type)
        instance.save()
        return instance

    

"""
class AdviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = FCMDevice
        fields = ('id','type','description','advice')
        read_only_fields = ['id','created_by', 'modified_by', 'created','modified']
"""