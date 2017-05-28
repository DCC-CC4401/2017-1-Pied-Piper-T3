# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Usuario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dispname = models.CharField(max_length=50)

class Vendedor(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    favoritos = models.IntegerField(default=0)
    #formas de pago
    efectivo = models.BooleanField()
    tcredito = models.BooleanField()
    tdebito = models.BooleanField()
    tjuna = models.BooleanField()
    #fin formas de pago
    fotoPerfil = models.CharField(max_length=200)

class VendedorAmbulante(models.Model):
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    activo = models.BooleanField()

class VendedorFijo(models.Model):
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    #si el vendedor fijo esta activo o no se calcula segun el horario actual y el horario registrado
    horaini = models.CharField(max_length=50)
    horafin = models.CharField(max_length=50)

class Alumno(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Producto(models.Model):
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    stock = models.IntegerField(default=0)
    precio = models.FloatField()
    descripcion = models.CharField(max_length=400)
    vendidos = models.IntegerField(default=0)
    categoria = models.CharField(max_length=50)

class Favorito(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)