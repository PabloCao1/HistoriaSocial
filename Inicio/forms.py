from django.contrib.auth.forms import AuthenticationForm

from django import forms
from .models import *


class OrganismosForm(forms.ModelForm):

    # borra todos los label
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
            
        self.fields['calle'].widget.attrs['placeholder'] = 'Calle'
        self.fields['altura'].widget.attrs['placeholder'] = 'Altura'
        self.fields['piso'].widget.attrs['placeholder'] = 'Piso'
       
    class Meta:
        model = Organismos
        
        exclude = ()
        # exclude = ('creado','modificado',)
        # widgets = {
        #     'obs' :                 forms.Textarea(attrs={'rows':3, 'placeholder': ''}),
        #     'nacionalidad':         forms.Select(),
        #     'fecha_nacimiento' :    forms.DateInput(attrs={'type': 'date'}, format="%Y-%m-%d"),
        # }


class CustomAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
        self.fields['username'].widget.attrs['placeholder'] = 'Usuario'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'

        
    class Meta:
        model = Usuarios
        fields=['__all__']