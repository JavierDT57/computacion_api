from django.shortcuts import render
from django.db.models import *
from django.db import transaction
from computacion_api.serializers import *
from computacion_api.models import *
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.utils.html import strip_tags
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from datetime import datetime
from django.conf import settings
from django.template.loader import render_to_string
import string
import random
import json

#Permite obtener toda la lista de Materias
class MateriasAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        materias = Materias.objects.filter().order_by("id")#Aca solo filtro por ID para su ordenamiento
        materias = MateriaSerializer(materias, many=True).data
        #Aquí convertimos los valores de nuevo a un array
        if not materias:
            return Response({},400)
        for materia in materias:
            materia["dias_json"] = json.loads(materia["dias_json"])

        return Response(materias, 200)

#Esta clase permite 
class MateriasView(generics.CreateAPIView):
    #Obtener usuario por ID
    # permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        materia = get_object_or_404(Materias, id = request.GET.get("id"))
        materia = MateriaSerializer(materia, many=False).data
        materia["dias_json"] = json.loads(materia["dias_json"])
        return Response(materia, 200)
    
    #Registrar nuevas materias
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        
        
        user = MateriaSerializer(data=request.data)
        if user.is_valid():
            #Grab user data
            nrc_materia = request.data['nrc_materia']
            #Valida si existe el usuario o bien el email registrado
            existing_user = User.objects.filter(nrc_materia=nrc_materia).first()

            if existing_user:
                return Response({"message":"Username "+nrc_materia+", is already taken"},400)

            user = User.objects.create( nrc_materia)
            
            
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        #Funcion para obtener los NRC de la BD y detectar que no se registren NRC repetidos
        nrc_materia = request.data.get('nrc_materia')  # Obtenemos el NRC de la solicitud
    
        # Validamos si el NRC proporcionado ya existe en la base de datos
        existing_materia = Materias.objects.filter(nrc_materia=nrc_materia).first()
        if existing_materia:
            return Response({"message": f"Materia con NRC {nrc_materia} ya existe"}, status=status.HTTP_400_BAD_REQUEST)
        
        #Creacion de funcion para poder registrar las materias en el modelo de materias en la BD
        #Create a profile for the user (Materia)
        materia = Materias.objects.create(
                                        nrc_materia = request.data["nrc_materia"],
                                        nombre_materia= request.data["nombre_materia"],
                                        hora_inicial= request.data["hora_inicial"],
                                        hora_final= request.data["hora_final"],
                                        seccion_materia= request.data["seccion_materia"],
                                        salon_materia= request.data["salon_materia"],
                                        programa_materia = request.data["programa_materia"],
                                        dias_json = json.dumps(request.data["dias_json"]))
        materia.save() #Guarda los datos en la base de datos

        return Response({"materia_created_id": materia.id }, 201)


#Funciones para editar y eliminar materias
class MateriasViewEdit(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def put(self, request, *args, **kwargs):
        # iduser=request.data["id"]
        materia = get_object_or_404(Materias, id=request.data["id"])
        materia.nrc_materia = request.data["nrc_materia"]
        materia.nombre_materia = request.data["nombre_materia"]
        materia.hora_inicial = request.data["hora_inicial"]
        materia.hora_final = request.data["hora_final"]
        materia.seccion_materia = request.data["seccion_materia"]
        materia.salon_materia = request.data["salon_materia"]
        materia.programa_materia = request.data["programa_materia"]
        materia.dias_json = json.dumps(request.data["dias_json"])
        materia.save()
        temp = materia.nrc_materia
        temp.save()
        user = MateriaSerializer(materia, many=False).data

        return Response(user,200)
    
    #Eliminar maestros
    def delete(self, request, *args, **kwargs):
        profile = get_object_or_404(Materias, id=request.GET.get("id"))
        try:
            profile.user.delete()
            return Response({"details":"Materia eliminada"},200)
        except Exception as e:            
            return Response({"details":"No se pudo eliminar la materia"},200)