# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def index(req):
    return render(req, 'app/index.html', {})

def login(req):
    return render(req, 'app/login.html', {})

def signup(req):
    return render(req, 'app/signup.html', {})

def vendedor(req):
    return render(req, 'app/vendedor-profile-page.html', {})

def gestion(req):
    return render(req, 'app/gestion-productos.html', {})

