from rest_framework import serializers
from myApp.models import DaysActivities, Schedules, Days
from collections import defaultdict

class DaysActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DaysActivities
        fields = '__all__'
        read_only_fields = ('days_activities_id',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Extracción de valores
        day_id = instance.days_activities_days.day_id
        day_description = instance.days_activities_days.day_description
        schedules_start = instance.days_activities_schedules.schedules_start
        schedules_end = instance.days_activities_schedules.schedules_end
        
        # Crear la estructura de respuesta
        response = {
            'day': {
                'id': day_id,
                'description': day_description,
                'schedules': []  # Inicializa la lista de horarios
            }
        }
        
        # Añadir el horario actual
        response['day']['schedules'].append({
            'start': schedules_start,
            'end': schedules_end,
        })
        
        return response

    # Crear un método que agrupe la información por día
    # def group_by_day(days_activities_queryset):
    #     grouped_data = defaultdict(lambda: {'description': '', 'schedules': []})

    #     for activity in days_activities_queryset:
    #         day_id = activity.days_activities_days.day_id
    #         day_description = activity.days_activities_days.day_description
    #         schedules_start = activity.days_activities_schedules.schedules_start
    #         schedules_end = activity.days_activities_schedules.schedules_end

    #         # Agrupar por día
    #         grouped_data[day_id]['description'] = day_description
    #         grouped_data[day_id]['schedules'].append({
    #             'start': schedules_start,
    #             'end': schedules_end,
    #         })
        
    #     # Convertir el defaultdict a un dict normal para la respuesta final
    #     return [{'id': day_id, **data} for day_id, data in grouped_data.items()]
    
class SchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedules
        fields = '__all__'
        read_only_fields = ('schedules_id',) # lectura
    
class DaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Days
        fields = '__all__'
        # read_only_fields = ('day_id',) # lectura