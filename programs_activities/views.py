from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from myApp.models import Areas, Programs, Activities, Objectives
from .serializers import AreasSerializer, ProgramsSerializer, ActivitiesSerializer, ObjectivesSerializer

class AreasViewSet(viewsets.ModelViewSet):
    queryset = Areas.objects.all()
    serializer_class = AreasSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        data = request.data

        user_id = request.user.id
        data['areas_user'] = user_id  

        serializer = self.get_serializer(data=data)

        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response({
            "message": "Area successfully created",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

class ProgramsViewSet(viewsets.ModelViewSet):
    queryset = Programs.objects.all()
    serializer_class = ProgramsSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data

        user_id = request.user.id
        data['programs_user'] = user_id  

        serializer = self.get_serializer(data=data)

        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response({
            "message": "Program successfully created",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
        
class ActivitiesViewSet(viewsets.ModelViewSet):
    queryset = Activities.objects.all()
    serializer_class = ActivitiesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data

        user_id = request.user.id
        data['activities_user'] = user_id

        # Crea una instancia del serializer con los datos actualizados
        serializer = self.get_serializer(data=data)

        # Valida los datos
        serializer.is_valid(raise_exception=True)

        # Guarda la nueva instancia de 'Activities'
        self.perform_create(serializer)

        # Devuelve una respuesta con un mensaje de éxito y los datos creados
        return Response({
            "message": "Actividad creada exitosamente",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    # Sobrescribe el método destroy para personalizar la respuesta al eliminar
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        
        # Devuelve un mensaje de confirmación
        return Response({
            "message": "Actividad eliminada exitosamente"
        }, status=status.HTTP_200_OK)

class ObjectivesViewSet(viewsets.ModelViewSet):
    queryset = Objectives.objects.all()
    serializer_class = ObjectivesSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_serializer(data=data)

        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response({
            "message": "Objective successfully created",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)