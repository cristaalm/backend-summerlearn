from rest_framework import serializers
from myApp.models import Areas, Programs


class AreasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Areas
        fields = '__all__'
        read_only_fields = ('areas_id',)

class ProgramsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programs
        fields = '__all__'
        read_only_fields = ('program_id',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['programs_user'] = {
            'id': instance.programs_user.id,
            'name': instance.programs_user.name,
            # Otros campos del usuario si los necesitas
        }
        return representation