from django import forms
from .models import *




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


