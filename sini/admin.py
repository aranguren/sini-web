from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

from .models import Contact, MobileWarning, Incidence, Advice, ApiGroup, ApiUser, Notification, IncidenceType, SiniFCMDevice

class WarningAdmin(LeafletGeoAdmin):
    #fields = ['name', 'geom']
    list_display = ('name','type_incidence','status','created','created_by_api_user','modified','modified_by_api_user')
    readonly_fields = ['created','created_by','modified','modified_by', 'created_by_api_user', 'modified_by_api_user','creation_origin']
    fieldsets = [
        #(None,               {'fields': ['question_text']}),
         ('Información Incidencia', {'fields': ['name','type_incidence','status','description', 'geom']}),
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
    list_display = ('name','type_incidence','status','created','created_by','modified','modified_by')
    readonly_fields = ['created','created_by','modified','modified_by']
    fieldsets = [
        #(None,               {'fields': ['question_text']}),
         ('Información Incidencia', {'fields': ['name','type_incidence','status','description', 'geom']}),
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


class UserDeviceInline(admin.TabularInline):
    model = SiniFCMDevice
    fields = ['name','device_id', 'registration_id', 'type', 'active']
    extra = 3 

class ApiUserAdmin(admin.ModelAdmin):
    #fields = ['name', 'geom']
    list_display = ('name','email','group', 'active')
    readonly_fields = ['password','password_str']
    fields  =[
        'name','email','group', 'password_str', 'active', 'is_anonymous',
    ]

    inlines = [UserDeviceInline,]


admin.site.register(ApiUser, ApiUserAdmin)


class SiniFCMDeviceAdmin(admin.ModelAdmin):
    #fields = ['name', 'geom']
    list_display = ('name','device_id','registration_id','type', 'user', 'active')
    fields  =[
        'name','device_id','registration_id','type', 'user', 'active'
    ]
    readonly_fields = ['created','modified']
 

admin.site.register(SiniFCMDevice, SiniFCMDeviceAdmin)

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


class ContactAdmin(admin.ModelAdmin):
    #fields = ['name', 'geom']
    list_display = ('name','email',
        'phone')
    
    fields  =[
        'name',
        'email',
        'description',
        'phone',
        'address'
    ]

    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)
 

admin.site.register(Contact, ContactAdmin)


class IncidenceTypeResource(resources.ModelResource):
    class Meta:
        model = IncidenceType
        skip_unchanged = True
        report_skipped = True
        exclude = ('created','created_by','modified','modified_by',)
        import_id_fields = ('name',)





class IncidenceTypeAdmin(ImportExportModelAdmin):
    resource_classes = [IncidenceTypeResource]
    #fields = ['name', 'geom']
    list_display = ('id','name')
    
    fields  =[
        'name'
    ]

    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)
 

admin.site.register(IncidenceType, IncidenceTypeAdmin)




