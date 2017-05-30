from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import datetime


class UserType(models.Model):
    type = models.CharField(max_length=15)

    def __str__(self):
        return self.type

class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)



class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    nombre = models.CharField(max_length=100)
    userType = models.ForeignKey(UserType, on_delete=models.CASCADE, default =4)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.nombre

    def get_short_name(self):
        return self.nombre

    def get_email(self):
        return self.email

    def get_user_type(self):
        return self.userType.id

    def vendedor(self):
        return Vendedor.objects.get(user=self)

    def consumidor(self):
        return ConsumidorProfile.objects.get(user=self)

    def is_consumidor(self):
        return self.get_user_type() == 3

    def is_movil(self):
        return self.get_user_type() == 2

    def is_fijo(self):
        return self.get_user_type() == 1

    def is_vendedor(self):
        return self.is_movil() or self.is_fijo()

    def get_avatar(self):
        return self.vendedor().avatar if self.is_vendedor() else self.consumidor().avatar

class Vendedor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    favoritos = models.IntegerField(default=0)
    avatar = models.ImageField(default='AvatarVendedor1.png')
    efectivo = models.BooleanField()
    debito = models.BooleanField()
    credito = models.BooleanField()
    junaeb = models.BooleanField()

    def __str__(self):
        return self.user.__str__()

    def is_fijo(self):
        return self.user.is_fijo()

    def is_movil(self):
        return self.user.is_movil()

    def horas(self):
        f = '%H:%M %p'
        return '{} - {}'.format(self.fijo().horaIni.strftime(f), self.fijo().horaFin.strftime(f)) if self.is_fijo() else ''

    def is_active_now(self):
        return self.fijo().horaIni < datetime.datetime.now().time() < self.fijo().horaFin if self.is_fijo() else self.movil().activo

    def fijo(self):
        return FijoProfile.objects.get(vendedor=self)

    def movil(self):
        return MovilProfile.objects.get(vendedor=self)


class ConsumidorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(default='AvatarEstudiante.png')

    def __str__(self):
        return self.user.__str__()


class MovilProfile(models.Model):
    vendedor = models.OneToOneField(Vendedor, on_delete=models.CASCADE)
    activo = models.BooleanField(default=False)

    def __str__(self):
        return self.vendedor.__str__()


class FijoProfile(models.Model):
    vendedor = models.OneToOneField(Vendedor, on_delete=models.CASCADE)
    horaIni = models.TimeField()
    horaFin = models.TimeField()

    def __str__(self):
        return self.vendedor.__str__()



class Favorito(models.Model):
    consumidor = models.ForeignKey(ConsumidorProfile, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)

class Categoria(models.Model):
    categoria = models.CharField(max_length=40)

class Productos(models.Model):
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    stock = models.IntegerField(default = 0)
    precio = models.IntegerField(default = 0)
    avatar = models.ImageField(default='bread.png')
    foto = models.ImageField()
    #Vendidos sirve para las estadisticas
    vendidos = models.IntegerField(default=0)
    enVenta = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre