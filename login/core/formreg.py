from django import forms
from . models import Usuario


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'email',
            'nombre',
            'apellido',
            'fecha_nacimiento',
            'dni',
            'telefono',
            'contraseña'
        ]