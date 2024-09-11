from rest_framework import viewsets
from rest_framework import permissions
from accounts.models import Areas, Programs
from .serializers import AreasSerializer, ProgramsSerializer

# Create your views here.

class AreasViewSet(viewsets.ModelViewSet):
    queryset = Areas.objects.all()
    serializer_class = AreasSerializer
    permission_classes = [permissions.AllowAny]

class ProgramsViewSet(viewsets.ModelViewSet):
    queryset = Programs.objects.all()
    serializer_class = ProgramsSerializer
    permission_classes = [permissions.AllowAny]