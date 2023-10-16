from django import forms
from .models import *
from leaflet.forms.widgets import LeafletWidget

from ckeditor.widgets import CKEditorWidget

LEAFLET_WIDGET_ATTRS = {
    'map_height': '700px',
    'map_width': '100%',
    'map_srid': 4326,
}

class ApiUserForm(forms.ModelForm):

    #group = forms.ModelChoiceField(queryset=ApiGroup.objects.exclude(name__iexact='api'))

    """
    def __init__(self,*args, user=None, **kwargs):
        super(ApiUserForm, self).__init__(*args, **kwargs)
        if not user.is_superuser:
            self.fields['group'].queryset = emp.objects.filter(branch=user.admin.branch_name)
    """

    class Meta:
        model = ApiUser
        exclude = ("id",'created_by', 'modified_by', 'password', 'password_str' )
        widgets = {
            #'name':forms.TextInput(attrs={'class': 'form-control'}),
            'name':forms.TextInput(attrs={'class': 'form-control'}),
            'email':forms.EmailInput(attrs={'class': 'form-control'}),
            'group':forms.Select(attrs={'class': 'form-select form-select-lg'}),
            }


class WarningForm(forms.ModelForm):


    class Meta:
        model = MobileWarning
        exclude = ("id",'created_by', 'modified_by', 
                   'created_by_api_user', 'modified_by_api_user',
                    'status','creation_origin', 'active' )
        widgets = {
            #'name':forms.TextInput(attrs={'class': 'form-control'}),
            'name':forms.TextInput(attrs={'class': 'form-control'}),
            'geom': LeafletWidget(attrs=LEAFLET_WIDGET_ATTRS),
            'type_incidence':forms.Select(attrs={'class': 'js-select2-simple form-select form-select-lg'}),
             'description':forms.Textarea(attrs={'class': 'form-control'}),
            #'active':forms.CheckboxInput(attrs={'class': 'form-check-input '}),
            'image1':forms.FileInput(attrs={'class': 'form-control'}),
            'image2':forms.FileInput(attrs={'class': 'form-control'}),
            'image3':forms.FileInput(attrs={'class': 'form-control'}),
            'audio':forms.FileInput(attrs={'class': 'form-control'}),
            'video':forms.FileInput(attrs={'class': 'form-control'})
            }


class IncidenceForm(forms.ModelForm):


    class Meta:
        model = Incidence
        exclude = ("id",'created_by', 'modified_by','status', 'active')
        
        widgets = {
            #'name':forms.TextInput(attrs={'class': 'form-control'}),
            'name':forms.TextInput(attrs={'class': 'form-control'}),
            'geom': LeafletWidget(attrs=LEAFLET_WIDGET_ATTRS),
            'type_incidence':forms.Select(attrs={'class': 'js-select2-simple form-select form-select-lg'}),
            'description':forms.Textarea(attrs={'class': 'form-control'}),
            #'active':forms.CheckboxInput(attrs={'class': 'form-check-input '}),
            'priority':forms.NumberInput(attrs={'class': 'form-control', 'min':1,'max': '5'}),
            'image1':forms.FileInput(attrs={'class': 'form-control'}),
            'image2':forms.FileInput(attrs={'class': 'form-control'}),
            'image3':forms.FileInput(attrs={'class': 'form-control'}),
            'audio':forms.FileInput(attrs={'class': 'form-control'}),
            'video':forms.FileInput(attrs={'class': 'form-control'})
            }


class AdviceForm(forms.ModelForm):


    class Meta:
        model = Advice
        exclude = ("id",'created_by', 'modified_by', )
        widgets = {
            #'name':forms.TextInput(attrs={'class': 'form-control'}),
            'name':forms.TextInput(attrs={'class': 'form-control'}),
            'description':forms.Textarea(attrs={'class': 'form-control'}),
            'advice':CKEditorWidget(attrs={'class': 'form-control'}),

            }




class NotificationForm(forms.ModelForm):


    class Meta:
        model = Notification
        exclude = ("id",'created_by', 'modified_by')
        
        widgets = {
            #'name':forms.TextInput(attrs={'class': 'form-control'}),
            'subject':forms.TextInput(attrs={'class': 'form-control'}),
            'geom': LeafletWidget(attrs=LEAFLET_WIDGET_ATTRS),
            'send_to':forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'message':forms.Textarea(attrs={'class': 'form-control'}),
            #'active':forms.CheckboxInput(attrs={'class': 'form-check-input '}),
            'url_noticia':forms.URLInput(attrs={'class': 'form-control'}),
            'url_imagen':forms.URLInput(attrs={'class': 'form-control'}),
             'api_user':forms.Select(attrs={'class': 'form-select form-select-lg'}),
             'api_group':forms.Select(attrs={'class': 'form-select form-select-lg'}),

            }