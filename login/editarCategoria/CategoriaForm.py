from django import forms
from core.models import Categoria



from django import forms
from core.models import Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'puntuacion']
        
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        instance = self.instance
        if 'nombre' in self.changed_data:  # Solo valida si el nombre ha cambiado
            if Categoria.objects.filter(nombre=nombre).exclude(id=instance.id).exists():
                raise forms.ValidationError("Ya existe una categoría con este nombre.")
        return nombre
    
    def clean_puntuacion(self):
        puntuacion = self.cleaned_data.get('puntuacion')
        if puntuacion <= 0:
            raise forms.ValidationError("La puntuación debe ser mayor a 0.")
        return puntuacion