# core/forms.py
from django import forms
from .models import Valoracion

class ValoracionForm(forms.ModelForm):
    class Meta:
        model = Valoracion
        fields = ['estrellas', 'comentario', 'solicitud']
        widgets = {
            'solicitud': forms.HiddenInput()  # Campo oculto para la solicitud
        }

    def __init__(self, *args, **kwargs):
        solicitud = kwargs.pop('solicitud', None)
        super().__init__(*args, **kwargs)
        if solicitud:
            self.fields['solicitud'].initial = solicitud
            self.fields['solicitud'].disabled = True  # Deshabilitar el campo para que no se pueda modificar
