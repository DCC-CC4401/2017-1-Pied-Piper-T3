from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.conf import settings
from .models import ConsumidorProfile, MovilProfile, FijoProfile, MyUser


class MyUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['email', 'password']



class ConsumidorForm(forms.ModelForm):
    class Meta:
        model = ConsumidorProfile
        fields = ['nombre', 'userType']


class MovilForm(forms.ModelForm):
    class Meta:
        model = MovilProfile
        fields = ['nombre', 'userType', 'efectivo', 'debito', 'credito', 'junaeb']


class FijoForm(forms.ModelForm):
    class Meta:
        model = FijoProfile
        fields = ['nombre', 'userType',  'horaIni', 'horaFin', 'efectivo', 'debito', 'credito', 'junaeb']

