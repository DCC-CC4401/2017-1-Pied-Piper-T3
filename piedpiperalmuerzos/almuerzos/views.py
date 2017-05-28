from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from .forms import *


def index(request):
    return render(request, 'almuerzos/index.html')


def base(request):
    return render(request, 'almuerzos/base.html')


def gestion_productos(request):
    return render(request, 'almuerzos/gestion_productos.html')


def signup(request):
    return render(request, 'almuerzos/signup.html')


def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('almuerzos/login.html', c)


def auth_view(request):
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=email, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/almuerzos/')
    else:
        return HttpResponseRedirect('/almuerzos/login/')


def registration(request):
    if request.method == "POST":
        uform = MyUserForm(request.POST)
        utype = request.POST.get('userType')
        if utype == "3":
            cform = ConsumidorForm(request.POST)

        elif utype == "2":
            cform = MovilForm(request.POST)

        elif utype == "1":
            cform = FijoForm(request.POST)

        cform.userType = int(utype)


        if uform.is_valid() and cform.is_valid():
            user = uform.save()
            user.set_password(user.password)
            user.save()
            profile = cform.save(commit = False)
            profile.user = user
            profile.save()
            return redirect('/almuerzos/')
        else:
            return redirect('/almuerzos/signup/')

    else:
        return redirect('/almuerzos/login/')





def vendedor_perfil(request):
    return render(request, 'almuerzos/vendedor_perfil.html')