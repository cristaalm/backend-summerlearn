from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from myApp.models import Areas, Programs, Activities, Objectives, Grades, SubscriptionsVolunteer
from .serializers import AreasSerializer, ProgramsSerializer, ActivitiesSerializer, ObjectivesSerializer, GradesSerializer,ActivitiesSerializer

# Import the function to export the data to Excel
from .utils.excel.programs.export_programs import export_programs_to_excel
from .utils.pdf.programs.export_programs import export_programs_to_pdf
from .utils.excel.activities.export_activities import export_activities_to_excel
from .utils.pdf.activities.export_activities import export_activities_to_pdf

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
    
    # custom action to get four last programs
    @action(detail=False, methods=['get'], url_path='last-programs')
    def last_programs(self, request):
        # Get the last 4 programs
        last_programs = Programs.objects.all().order_by('-programs_id')[:6]
        # Serialize the data
        serializer = ProgramsSerializer(last_programs, many=True)
        # Return the data
        return Response(serializer.data)
    
    #?######################## Exportar a Excel y PDF ########################
    
    @action(detail=False, methods=['get'], url_path='exportar-excel') # http://localhost:8000/programs/exportar-excel/
    def exportar_programs_excel(self, request):
        return export_programs_to_excel()
    
    @action(detail=False, methods=['get'], url_path='exportar-pdf') # http://localhost:8000/programs/exportar-pdf/
    def exportar_programs_pdf(self, request):
        return export_programs_to_pdf()
    

class ActivitiesViewSet(viewsets.ModelViewSet):
    queryset = Activities.objects.all()
    serializer_class = ActivitiesSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # Creación de una actividad
    def create(self, request, *args, **kwargs):
        # Crear el serializer con los datos proporcionados
        serializer = self.get_serializer(data=request.data)
        
        # Validar los datos
        serializer.is_valid(raise_exception=True)
        
        # Guardar la nueva instancia de 'Activities'
        self.perform_create(serializer)
        
        # Retornar una respuesta con un mensaje de éxito y los datos creados
        return Response({
            "message": "Actividad creada exitosamente",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    # Personalización de la respuesta al eliminar una actividad
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        
        # Retornar un mensaje de confirmación
        return Response({
            "message": "Actividad eliminada exitosamente"
        }, status=status.HTTP_200_OK)

    # Endpoint personalizado para obtener actividades con el estado de suscripción del usuario
    @action(detail=False, methods=['get'], url_path='activities-subscribed')
    def activitiesSubscribed(self, request):
        id_user = request.query_params.get('id_user', None)

        if not id_user:
            return Response({'error': 'id_user no proporcionado'}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener todas las suscripciones del usuario actual
        subs = SubscriptionsVolunteer.objects.filter(
            subscriptions_volunteer_user=id_user
        )
        subs_ids = subs.values_list('subscriptions_volunteer_activity', flat=True)

        # Verificar si el usuario tiene exactamente 3 suscripciones
        if subs.count() == 3:
            # Filtrar solo las actividades a las que el usuario está suscrito
            actividades = Activities.objects.filter(activities_id__in=subs_ids)
        else:
            # Obtener todas las actividades
            actividades = Activities.objects.all()

        # Crear una lista de actividades con el estado de suscripción
        actividades_data = []
        for actividad in actividades:
            suscrito = actividad.activities_id in subs_ids  # Verifica si está suscrito
            actividades_data.append({
                'activities_id': actividad.activities_id,
                'activities_name': actividad.activities_name,
                'activities_description': actividad.activities_description,
                'activities_program': actividad.activities_program.programs_name,
                'activities_program_area': actividad.activities_program.programs_area.areas_name,
                'activities_status': actividad.activities_status,
                'suscrito': suscrito  # True si está suscrito, False si no lo está
            })

        # Retornar las actividades con el estado de suscripción en formato JSON
        return Response(actividades_data, status=status.HTTP_200_OK)

    
    #?######################## Exportar a Excel y PDF ########################

    @action(detail=False, methods=['get'], url_path='exportar-excel') # http://localhost:8000/activities/exportar-excel/
    def exportar_activities_excel(self, request):
        return export_activities_to_excel()
    
    @action(detail=False, methods=['get'], url_path='exportar-pdf') # http://localhost:8000/activities/exportar-pdf/
    def exportar_activities_pdf(self, request):
        return export_activities_to_pdf()
    

class ObjectivesViewSet(viewsets.ModelViewSet):
    queryset = Objectives.objects.all()  # Consulta de todos los objetivos
    serializer_class = ObjectivesSerializer  # Serializer para los objetivos
    permission_classes = [permissions.IsAuthenticated]  # Requiere autenticación
    authentication_classes = [JWTAuthentication]  # Usa JWT para la autenticación
    
    # Método para crear un objetivo
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            "message": "Objective successfully created",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    # Acción personalizada para obtener objetivos filtrados por 'id_activity'
    @action(detail=False, methods=['get'], url_path='get-objectives')
    def objectivesByActivity(self, request):
        id_activity = request.query_params.get('id_activity', None)
        if id_activity:
            # Filtrar objetivos por id_activity y devolver solo los campos 'id' y 'description'
            objectives_by_activity = Objectives.objects.filter(objectives_activity=id_activity).values('objectives_id', 'objectives_description')
            return Response(objectives_by_activity)  # Retorna un JSON con los objetivos filtrados
        else:
            return Response({'error': 'id_activity no proporcionado'}, status=400)
        
class GradesViewSet(viewsets.ModelViewSet):
    queryset = Grades.objects.all()
    serializer_class = GradesSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]