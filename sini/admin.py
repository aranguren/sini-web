from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

# Register your models here.

from .models import Incidencia


class IncidenciaAdmin(LeafletGeoAdmin):
    #fields = ['name', 'geom']
    list_display = ('name','tipo_incidente','status','created','created_by','modified','modified_by')
    readonly_fields = ['created','created_by','modified','modified_by']
    fieldsets = [
        #(None,               {'fields': ['question_text']}),
         ('Información Incidencia', {'fields': ['name','tipo_incidente','status','descripcion', 'geom']}),
        ('Archivos', {'fields': ['foto1','foto2','foto3','audio', 'video']}),
         ('Informacion registro BD', {'fields': ['created','created_by','modified','modified_by']}),
         
    ]

    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Incidencia, IncidenciaAdmin)
