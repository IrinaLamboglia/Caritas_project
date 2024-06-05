from datetime import date
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
            'filial_nombre',
        ]

    def clean_email(self):
        email = self.cleaned_data['email']
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email

    def clean_contraseña(self):
        contraseña = self.cleaned_data['contraseña']
        if len(contraseña) < 6:
            raise forms.ValidationError("La contraseña debe tener al menos 6 caracteres.")
        return contraseña

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data['fecha_nacimiento']
        edad = date.today().year - fecha_nacimiento.year - ((date.today().month, date.today().day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        if edad < 18:
            raise forms.ValidationError("Debes tener al menos 18 años para registrarte.")
        return fecha_nacimiento


    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.username = self.cleaned_data['email']  # Establecer el correo electrónico como nombre de usuario
        usuario.puntuacion=3
        if commit:
            usuario.save()
        return usuario
    
    def clean_filial(self):
        filial = self.cleaned_data['filial_nombre']
        # Validar la filial solo si se proporciona y el usuario es de tipo 'ayudante'
        if filial and self.instance.tipo == 'administrador':
            if Usuario.objects.filter(filial_nombre=filial).exists():
                raise forms.ValidationError("Ya existe un usuario registrado en esta filial.")
        return filial