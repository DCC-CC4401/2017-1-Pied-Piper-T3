from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings



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
        return self.email

    def get_short_name(self):
        return self.email


class UserType(models.Model):
    type = models.CharField(max_length=15,)


class Vendedor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    favoritos = models.IntegerField(default=0)
    avatar = models.ImageField(default='almuerzos/static/img/AvatarVendedor1.png')
    efectivo = models.BooleanField()
    debito = models.BooleanField()
    credito = models.BooleanField()
    junaeb = models.BooleanField()


class ConsumidorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    userType = models.ForeignKey(UserType, on_delete=models.CASCADE)
    avatar = models.ImageField(default='almuerzos/static/img/AvatarEstudiante.png')


class MovilProfile(models.Model):
    vendedor = models.OneToOneField(Vendedor, on_delete=models.CASCADE)
    userType = models.ForeignKey(UserType, on_delete=models.CASCADE)
    activo = models.BooleanField(default=False)


class FijoProfile(models.Model):
    vendedor = models.OneToOneField(Vendedor, on_delete=models.CASCADE)
    userType = models.ForeignKey(UserType, on_delete=models.CASCADE)
    horaIni = models.TimeField()
    horaFin = models.TimeField()


class Favorito(models.Model):
    consumidor = models.ForeignKey(ConsumidorProfile, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)


class Productos(models.Model):
    vendedor = models.OneToOneField(Vendedor)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100)
    stock = models.IntegerField(default = 0)
    precio = models.IntegerField(default = 0)
    avatar = models.ImageField(default='almuerzos/static/img/bread.png')
    foto = models.ImageField(upload_to='almuerzos/productos/', default='almuerzos/static/img/background4.png')
    #Vendidos sirve para las estadisticas
    vendidos = models.IntegerField(default=0)
    enVenta = models.BooleanField(default=False)

#User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
