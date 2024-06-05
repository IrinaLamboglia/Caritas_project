from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Create your models here.



class FailedLoginAttempt(models.Model):
    email = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)





class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    dni = models.CharField(max_length=10)
    telefono = models.CharField(max_length=10)
    contraseña = models.CharField(max_length=128, validators=[MinLengthValidator(6)], default='valor_predeterminado')  # Campo para almacenar la contraseña cifrada
    last_login = models.DateTimeField(verbose_name='last login', blank=True, null=True)
    tipo= models.CharField(max_length=30, default="")
    puntuacion = models.DecimalField(max_digits=10, decimal_places=2)



class UsuarioBloqueado(models.Model):
    email= models.EmailField(unique=True)


class porDesbloquear(models.Model):
    email= models.EmailField(unique=True)  
    
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre



class Publicacion(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=400)
    nuevo = models.BooleanField(default=True)
    estado = models.BooleanField(default=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null = True)
    imagen = models.ImageField(upload_to='media/publicaciones/', null=True, blank=True)

    def __str__(self):
        return self.titulo
    
email= models.EmailField(unique=True)



class Solicitud(models.Model):
    solicitante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='solicitudes')
    fecha_solicitud = models.DateTimeField(default=timezone.now)
    estado = models.BooleanField(default=False)
    publicacionOfrecida = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='ofrecimientos')
    realizado= models.BooleanField(default=False)

    def __str__(self):
        return f"{self.solicitante} solicita {self.publicacion}"