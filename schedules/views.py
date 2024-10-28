from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from myApp.models import DaysActivities, Schedules, Days
from .serializers import DaysActivitiesSerializer, SchedulesSerializer, DaysSerializer
from collections import defaultdict

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
        
class SchedulesSerializer(viewsets.ModelViewSet):
    queryset = Schedules.objects.all()
    serializer_class = SchedulesSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response({
            "message": "Schedule successfully created",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
        
class DaysViewSet(viewsets.ModelViewSet):  # Renamed the class to avoid naming conflict
    queryset = Days.objects.all()
    serializer_class = DaysSerializer
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

    @action(detail=False, methods=['get'], url_path='get-days')
    def days_by_activity(self, request):
        id_activity = request.query_params.get('id_activity', None)

        if id_activity:
            booked_days = DaysActivities.objects.filter(days_activities_activity=id_activity).values_list('days_activities_days_id', flat=True)
            available_days = Days.objects.exclude(day_id__in=booked_days)

            serializer = DaysSerializer(available_days, many=True)

            return Response({
                "available_days": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'id_activity not provided'}, status=status.HTTP_400_BAD_REQUEST)