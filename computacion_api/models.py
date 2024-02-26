from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

class BearerTokenAuthentication(TokenAuthentication):
    keyword = u"Bearer"


class Administradores(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    clave_admin = models.CharField(max_length=255,null=True, blank=True)#ID del administrador
    telefono = models.CharField(max_length=255, null=True, blank=True)#telefono
    rfc = models.CharField(max_length=255,null=True, blank=True)#RFC
    edad = models.IntegerField(null=True, blank=True)#edad
    ocupacion = models.CharField(max_length=255,null=True, blank=True)#ocupacion
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)#fecha de creacion del registro
    update = models.DateTimeField(null=True, blank=True)#fecha de actualizacion del registro

    def __str__(self):
        return "Perfil del admin "+self.first_name+" "+self.last_name
    
    
class Alumnos(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    matricula = models.CharField(max_length=255,null=True, blank=True)#matricula del alumno
    fecha_nacimiento = models.DateTimeField(auto_now_add=False,null=True, blank=True)#fecha de nacimiento
    curp = models.CharField(max_length=255,null=True, blank=True)#CURP
    rfc = models.CharField(max_length=255,null=True, blank=True)#RFC
    edad = models.IntegerField(null=True, blank=True)#edad
    telefono = models.CharField(max_length=255, null=True, blank=True)#telefono
    ocupacion = models.CharField(max_length=255,null=True, blank=True)#ocupacion
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)#fecha de creacion del registro
    update = models.DateTimeField(null=True, blank=True)#fecha de actualizacion del registro

    def __str__(self):
        return "Perfil del alumno "+self.first_name+" "+self.last_name    


class Maestros(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    id_trabajador = models.CharField(max_length=255,null=True, blank=True)#matricula del alumno
    fecha_nacimiento = models.DateTimeField(auto_now_add=False,null=True, blank=True)#fecha de nacimiento
    telefono = models.CharField(max_length=255, null=True, blank=True)#telefono
    rfc = models.CharField(max_length=255,null=True, blank=True)#RFC
    cubiculo = models.CharField(max_length=255,null=True, blank=True)#cubiculo
    area_investigacion = models.CharField(max_length=255,null=True, blank=True)#area de investigacion
    materias_json = models.TextField(null=True, blank=True)#materias para seleccionar y estan en un arreglo json, por asi el inicio de la variable
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)#fecha de creacion del registro
    update = models.DateTimeField(null=True, blank=True)#fecha de actualizacion del registro

    def __str__(self):
        return "Perfil del maestro "+self.first_name+" "+self.last_name  