from .controllers.serializers import RolSeralizer, StatusSerializer, UsersSerializer
from myApp.models import Rol, Status, Users
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

###############Ver lista de usuarios###############

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def user_list(request):
    if request.method == 'GET':
        user_all = Users.objects.all()  # Obtiene todos los usuarios
        serializer = UsersSerializer(user_all, many=True)  # Serializa los datos
        return Response(serializer.data)  # Devuelve la respuesta en JSON

###############Ver lista de status###############

@api_view(['GET',])
@permission_classes((permissions.AllowAny,))
def status_list(request):
    if request.method == 'GET':
        status = Status.objects.all() 
        serializer = StatusSerializer(status, many=True)
        return Response(serializer.data)

###############Ver lista de roles###############

@api_view(['GET',])
@permission_classes((permissions.AllowAny,))
def rol_list(request):
    if request.method == 'GET':
        rol = Rol.objects.all()
        serializer = RolSeralizer(rol, many=True)
        return Response(serializer.data)
