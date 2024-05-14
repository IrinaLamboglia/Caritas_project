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
            'contraseña',
            'filial'
        ]
    def clean_filial(self):
        filial = self.cleaned_data['filial']
        if Usuario.objects.filter(filial=filial).exists():
            raise forms.ValidationError("Ya existe un usuario registrado en esta filial.")
        return filial

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.username = self.cleaned_data['email']  # Establecer el correo electrónico como nombre de usuario
        if commit:
            usuario.save()
        return usuario