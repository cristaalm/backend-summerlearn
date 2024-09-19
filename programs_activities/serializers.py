from rest_framework import serializers
from myApp.models import Areas, Programs, Activities, Objectives


class AreasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Areas
        fields = '__all__'
        read_only_fields = ('areas_id',)

class ProgramsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programs
        fields = '__all__'
        read_only_fields = ('programs_id',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['programs_user'] = {
            'id': instance.programs_user.id,
            'name': instance.programs_user.name,
        }
        return representation
    
class ActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activities
        fields = '__all__'
        read_only_fields = ('activities_id',) # lectura

    def to_representation(self, instance): # es sobrescrito para personalizar cómo se representa el objeto
        representation = super().to_representation(instance)
        representation['activities_program'] = {
            'id': instance.activities_program.programs_id,
            'name': instance.activities_program.programs_name,
        }
        representation['activities_user'] = {
            'id': instance.activities_user.id,
            'name': instance.activities_user.name,
        }
        representation['activities_area'] = {
            'id': instance.activities_area.areas_id,
            'name': instance.activities_area.areas_name,
        }
        return representation

class ObjectivesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objectives
        fields = '__all__'
        read_only_fields = ('objectives_id',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['objectives_activity'] = {
            'id': instance.objectives_activity.activities_id,
            'name': instance.objectives_activity.activities_name,
        }
        return representation