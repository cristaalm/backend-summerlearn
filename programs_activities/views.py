from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from myApp.models import Areas, Programs, Activities, Objectives
from .serializers import AreasSerializer, ProgramsSerializer, ActivitiesSerializer, ObjectivesSerializer

from .utils.excel.programs.export_programs import export_programs_to_excel
from .utils.pdf.programs.export_programs import export_programs_to_pdf

class AreasViewSet(viewsets.ModelViewSet):
    queryset = Areas.objects.all()
    serializer_class = AreasSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response({
            "message": "Area successfully created",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

class ProgramsViewSet(viewsets.ModelViewSet):
    queryset = Programs.objects.all()
    serializer_class = ProgramsSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response({
            "message": "Program successfully created",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'], url_path='exportar-excel') # http://localhost:8000/programs/exportar-excel
    def exportar_programs_excel(self, request):
        return export_programs_to_excel()
    
    @action(detail=False, methods=['get'], url_path='exportar-pdf') # http://localhost:8000/programs/exportar-pdf
    def exportar_programs_pdf(self, request):
        return export_programs_to_pdf()
        
        
class ActivitiesViewSet(viewsets.ModelViewSet):
    queryset = Activities.objects.all()
    serializer_class = ActivitiesSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        # Create a serializer instance with the provided data
        serializer = self.get_serializer(data=request.data)

        # Validate the data
        serializer.is_valid(raise_exception=True)

        # Save the new 'Activities' instance
        self.perform_create(serializer)

        # Return a response with a success message and the created data
        return Response({
            "message": "Actividad creada exitosamente",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    # Override the destroy method to customize the response when deleting
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        
        # Return a confirmation message
        return Response({
            "message": "Actividad eliminada exitosamente"
        }, status=status.HTTP_200_OK)

class ObjectivesViewSet(viewsets.ModelViewSet):
    queryset = Objectives.objects.all()
    serializer_class = ObjectivesSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response({
            "message": "Objective successfully created",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)