from django import forms
from .models import Publicacion

class ProductoDonadoForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['titulo', 'descripcion','nuevo', 'categoria', 'stock']

   