from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf


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
    user = auth.authenticate(email=email, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/almuerzos/')
    else:
        return HttpResponseRedirect('/almuerzos/login/')



def vendedor_perfil(request):
    return render(request, 'almuerzos/vendedor_perfil.html')