from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

# Register your models here.

from .models import Incidence


class IncidenceAdmin(LeafletGeoAdmin):
    #fields = ['name', 'geom']
    list_display = ('name','incidence_type','status','created','created_by','modified','modified_by')
    readonly_fields = ['created','created_by','modified','modified_by']
    fieldsets = [
        #(None,               {'fields': ['question_text']}),
         ('Información Incidencia', {'fields': ['name','incidence_type','status','description', 'geom']}),
        ('Archivos', {'fields': ['image1','image2','image3','audio', 'video']}),
         ('Informacion registro BD', {'fields': ['created','created_by','modified','modified_by']}),
         
    ]

    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Incidence, IncidenceAdmin)
