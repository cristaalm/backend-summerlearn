from django.http import JsonResponse
from django.shortcuts import render

from myApp.models import Rol, Status
from .models import Users
from .serialize import RolSeralizer, StatusSerializer, UserSerializer
from rest_framework import viewsets, permissions
# Create your views here.


def index(request):
    return render(request, 'index.html')


class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all() # Define la consulta que será ejecutada por el ViewSet
    permission_classes = [permissions.AllowAny]# Define la lista de permisos requeridos para acceder a la vista
    serializer_class = UserSerializer# Define el serializador que será utilizado por el ViewSet


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = StatusSerializer

class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RolSeralizer