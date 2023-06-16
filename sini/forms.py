from django import forms
from .models import *
from leaflet.forms.widgets import LeafletWidget

LEAFLET_WIDGET_ATTRS = {
    'map_height': '700px',
    'map_width': '100%',
    'map_srid': 4326,
}

class ApiUserForm(forms.ModelForm):


    class Meta:
        model = ApiUser
        exclude = ("id",'created_by', 'modified_by', 'password', 'password_str' )
        widgets = {
            #'name':forms.TextInput(attrs={'class': 'form-control'}),
            'name':forms.TextInput(attrs={'class': 'form-control'}),
            'email':forms.EmailInput(attrs={'class': 'form-control'}),
            'group':forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'token_fcm':forms.TextInput(attrs={'class': 'form-control'}),

            }


class WarningForm(forms.ModelForm):


    class Meta:
        model = MobileWarning
        exclude = ("id",'created_by', 'modified_by', 
                   'created_by_api_user', 'modified_by_api_user',
                    'status','creation_origin' )
        widgets = {
            #'name':forms.TextInput(attrs={'class': 'form-control'}),
            'name':forms.TextInput(attrs={'class': 'form-control'}),
            'geom': LeafletWidget(attrs=LEAFLET_WIDGET_ATTRS),
            'incidence_type':forms.Select(attrs={'class': 'form-select form-select-lg'}),
             'description':forms.Textarea(attrs={'class': 'form-control'}),
            'active':forms.CheckboxInput(attrs={'class': 'form-check-input '}),
            'image1':forms.FileInput(attrs={'class': 'form-control'}),
            'image2':forms.FileInput(attrs={'class': 'form-control'}),
            'image3':forms.FileInput(attrs={'class': 'form-control'}),
            'audio':forms.FileInput(attrs={'class': 'form-control'}),
            'video':forms.FileInput(attrs={'class': 'form-control'})
            }


class IncidenceForm(forms.ModelForm):


    class Meta:
        model = Incidence
        exclude = ("id",'created_by', 'modified_by','status')
        
        widgets = {
            #'name':forms.TextInput(attrs={'class': 'form-control'}),
            'name':forms.TextInput(attrs={'class': 'form-control'}),
            'geom': LeafletWidget(attrs=LEAFLET_WIDGET_ATTRS),
            'incidence_type':forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'description':forms.Textarea(attrs={'class': 'form-control'}),
            'active':forms.CheckboxInput(attrs={'class': 'form-check-input '}),
            'image1':forms.FileInput(attrs={'class': 'form-control'}),
            'image2':forms.FileInput(attrs={'class': 'form-control'}),
            'image3':forms.FileInput(attrs={'class': 'form-control'}),
            'audio':forms.FileInput(attrs={'class': 'form-control'}),
            'video':forms.FileInput(attrs={'class': 'form-control'})
            }
