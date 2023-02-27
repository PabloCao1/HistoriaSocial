
from django import forms
from .models import *


class LegajosForm(forms.ModelForm):

    #borra todos los label
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
        self.fields['sexo'].widget.attrs['placeholder'] = 'Como figure en el DNI'
    
    
    
    class Meta:
        model = Legajos
        exclude = ('creado','modificado',)
        widgets = {
            # 'obs' :                 forms.Textarea(attrs={'rows':3, 'placeholder': ''}),
            # 'nacionalidad':         forms.Select(),
            # 'fecha_nacimiento' :    forms.DateInput(attrs={'type': 'date'}, format="%Y-%m-%d"),
        }