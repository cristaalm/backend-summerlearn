from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from myApp.models import DaysActivities, Schedules, Days, Activities
from .serializers import DaysActivitiesSerializer, SchedulesSerializer, DaysSerializer
from collections import defaultdict
from django.db.models import OuterRef, Subquery, Count, F

class DaysActivitiesSerializer(viewsets.ModelViewSet):
    queryset = DaysActivities.objects.all()
    serializer_class = DaysActivitiesSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            "message": "Day successfully created",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='get-schedules-activity')
    def objectivesByActivity(self, request):
        id_activity = request.query_params.get('id_activity', None)

        if id_activity:
            # Filtrar los objetivos por la actividad dada
            objectives_by_activity = DaysActivities.objects.filter(days_activities_activity=id_activity)

            # Agrupar los datos por día usando el método group_by_day
            grouped_data = self.group_by_day(objectives_by_activity)

            # Retornar la respuesta con los datos agrupados
            return Response(grouped_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'id_activity not provided'}, status=status.HTTP_400_BAD_REQUEST)

    # Método para agrupar datos por día
    def group_by_day(self, days_activities_queryset):
        grouped_data = defaultdict(lambda: {'description': '', 'schedules': []})

        for activity in days_activities_queryset:
            day_id = activity.days_activities_days.day_id
            day_description = activity.days_activities_days.day_description
            schedules_start = activity.days_activities_schedules.schedules_start
            schedules_end = activity.days_activities_schedules.schedules_end

            # Agrupar los horarios por día
            grouped_data[day_id]['description'] = day_description
            grouped_data[day_id]['schedules'].append({
                'start': schedules_start,
                'end': schedules_end,
            })

        # Ordenar los horarios por schedules_end
        for data in grouped_data.values():
            data['schedules'].sort(key=lambda x: x['end'])  # Ordenar por 'end'

        # Convertir el defaultdict a una lista normal para la respuesta final
        return [{'id': day_id, **data} for day_id, data in grouped_data.items()]
        
class SchedulesViewSet(viewsets.ModelViewSet):
    queryset = Schedules.objects.all()
    serializer_class = SchedulesSerializer

    @action(detail=False, methods=['get'], url_path='get-available-schedules')
    def get_available_schedules(self, request):
        id_activity = request.query_params.get('id_activity')
        id_day = request.query_params.get('id_day')

        if not id_activity or not id_day:
            return Response({'error': 'id_activity and id_day are required'}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Obtiene el programa de la actividad seleccionada
        try:
            activity = Activities.objects.get(activities_id=id_activity)
            id_program = activity.activities_program
        except Activities.DoesNotExist:
            return Response({'error': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)

        # 2. Obtiene todos los IDs de actividad asociados con el programa
        related_activities = Activities.objects.filter(activities_program=id_program).values_list('activities_id', flat=True)
        print("IDs de actividades relacionadas:", related_activities)

        # 3. Itera sobre cada ID de actividad, buscando los horarios reservados para cada uno en el día especificado
        all_booked_schedules = []
        for related_activity_id in related_activities:
            booked_schedules = DaysActivities.objects.filter(
                days_activities_activity_id=related_activity_id,
                days_activities_days_id=id_day
            ).values_list('days_activities_schedules_id', flat=True)
            print(f"Horarios reservados para actividad {related_activity_id} en día {id_day}:", booked_schedules)
            all_booked_schedules.extend(booked_schedules)

        # 4. Obtiene solo los IDs de horarios únicos
        unique_booked_schedules = list(set(all_booked_schedules))
        print("IDs únicos de horarios reservados:", unique_booked_schedules)

        # 5. Excluye los horarios reservados y devuelve los no reservados
        available_schedules = Schedules.objects.exclude(schedules_id__in=unique_booked_schedules)

        # Serializa y devuelve los horarios disponibles
        serializer = SchedulesSerializer(available_schedules, many=True)
        return Response({
            "available_schedules": serializer.data
        }, status=status.HTTP_200_OK)

        
class DaysViewSet(viewsets.ModelViewSet):
    queryset = Days.objects.all()
    serializer_class = DaysSerializer

    @action(detail=False, methods=['get'], url_path='get-unused-days')
    def get_unused_days(self, request):
        id_activity = request.query_params.get('id_activity')
        
        if not id_activity:
            return Response({'error': 'id_activity is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Busca los días ya usados para esta actividad
        used_days = DaysActivities.objects.filter(
            days_activities_activity_id=id_activity
        ).values_list('days_activities_days_id', flat=True)

        # Obtén los días que no están en la lista de días ya usados
        unused_days = Days.objects.exclude(day_id__in=used_days)

        # Serializa y devuelve los días no usados
        serializer = DaysSerializer(unused_days, many=True)
        return Response({
            "unused_days": serializer.data
        }, status=status.HTTP_200_OK)