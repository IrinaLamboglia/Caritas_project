from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser

# Create your models here.



#uso la bd de django para almacenar los intentos fallidos para el inicio de sesion
class FailedLoginAttempt(models.Model):
    email = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)



#para registro
#  ingresa nombre de usuario “martinacolombo@gmail.com”,
# contraseña “Marti2”, dni “44851840”, 
# fecha de nacimiento:06/05/2003, 
# teléfono “222884345”,
# Nombre y
# Apellido: Martina colombo y presiona “aceptar”

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
  #  USERNAME_FIELD = 'email'
   # REQUIRED_FIELDS = []



class UsuarioBloqueado(models.Model):
    email= models.EmailField(unique=True)


#opciones de rol que vamos a necesitar mas adelante



class porDesbloquear(models.Model):
   email= models.EmailField(unique=True)
   
   
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')

    def __str__(self):
        return self.nombre    
    