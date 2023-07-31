from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

# Register your models here.

from .models import MobileWarning, Incidence, Advice, ApiGroup, ApiUser, Notification

class WarningAdmin(LeafletGeoAdmin):
    #fields = ['name', 'geom']
    list_display = ('name','incidence_type','status','created','created_by_api_user','modified','modified_by_api_user')
    readonly_fields = ['created','created_by','modified','modified_by', 'created_by_api_user', 'modified_by_api_user','creation_origin']
    fieldsets = [
        #(None,               {'fields': ['question_text']}),
         ('Información Incidencia', {'fields': ['name','incidence_type','status','description', 'geom']}),
        ('Archivos', {'fields': ['image1','image2','image3','audio', 'video']}),
         ('Informacion registro BD', {'fields': ['creation_origin', 'created','created_by','modified','modified_by','created_by_api_user', 'modified_by_api_user']}),
         
    ]

    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = request.user
            obj.creation_origin='web'
        super().save_model(request, obj, form, change)


admin.site.register(MobileWarning, WarningAdmin)




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


class AdviceAdmin(admin.ModelAdmin):
    #fields = ['name', 'geom']
    list_display = ('name','description')
    readonly_fields = ['created','created_by','modified','modified_by']

    fields  =[
        'name','description','advice'
    ]

admin.site.register(Advice, AdviceAdmin)

class ApiUserAdmin(admin.ModelAdmin):
    #fields = ['name', 'geom']
    list_display = ('name','email','group', 'active')
    readonly_fields = ['password','password_str']
    fields  =[
        'name','email','group', 'password_str', 'active', 'device'
    ]
 




admin.site.register(ApiUser, ApiUserAdmin)

class ApiGroupAdmin(admin.ModelAdmin):
    #fields = ['name', 'geom']
    list_display = ('name',)
    fields  =[
        'name'
    ]
 




admin.site.register(ApiGroup, ApiGroupAdmin)



class NotificationAdmin(LeafletGeoAdmin):
    #fields = ['name', 'geom']
    list_display = ('subject','send_to',
        'api_user',
        'api_group')
    
    fields  =[
        'subject',
        'send_to',
        'api_user',
        'api_group',
        'url_noticia',
        'url_imagen',
        'message',
        'geom'
    ]

    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)
 




admin.site.register(Notification, NotificationAdmin)