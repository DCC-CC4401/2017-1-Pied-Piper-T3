from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.conf import settings
from .models import ConsumidorProfile, MovilProfile, FijoProfile, MyUser, Vendedor, Productos


class MyUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['userType', 'nombre', 'email', 'password']



class VendedorForm(forms.ModelForm):
    avatar = forms.ImageField(required = False)
    class Meta:
        model = Vendedor
        fields = ['avatar', 'efectivo', 'debito', 'credito', 'junaeb']


class ConsumidorForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)
    class Meta:
        model = ConsumidorProfile
        fields = ['avatar']

class MovilForm(forms.ModelForm):
    class Meta:
        model = MovilProfile
        fields = ['activo']


class FijoForm(forms.ModelForm):
    class Meta:
        model = FijoProfile
        fields = ['horaIni', 'horaFin']

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Productos
        fields = ['nombre', 'precio', 'stock', 'categoria', 'descripcion', 'avatar', 'foto']

