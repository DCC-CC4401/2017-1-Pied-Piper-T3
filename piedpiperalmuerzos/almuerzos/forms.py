from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.conf import settings
from .models import ConsumidorProfile, MovilProfile, FijoProfile, MyUser, Vendedor


class MyUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['nombre', 'email', 'password']



class VendedorForm(forms.ModelForm):
    class Meta:
        model = Vendedor
        fields = ['efectivo', 'debito', 'credito', 'junaeb']


class ConsumidorForm(forms.ModelForm):
    class Meta:
        model = ConsumidorProfile
        fields = ['userType']


class MovilForm(forms.ModelForm):
    class Meta:
        model = MovilProfile
        fields = ['userType']


class FijoForm(forms.ModelForm):
    class Meta:
        model = FijoProfile
        fields = ['userType',  'horaIni', 'horaFin']

