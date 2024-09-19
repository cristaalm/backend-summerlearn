from rest_framework import serializers
from myApp.models import DaysActivities, Schedules

class DaysActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DaysActivities
        fields = '__all__'
        read_only_fields = ('days_activities_id',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['days_activities_activity'] = {
            'id': instance.days_activities_activity.activities_id,
            'name': instance.days_activities_activity.activities_name,
        }
        representation['days_activities_days'] = {
            'id': instance.days_activities_days.day_id,
            'description': instance.days_activities_days.day_description,
        }
        return representation
    
class SchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedules
        fields = '__all__'
        read_only_fields = ('schedules_id',) # lectura

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['schedules_day'] = {
            'id': instance.schedules_day.days_activities_id,
            'day': instance.schedules_day.days_activities_days,
        }
        return representation