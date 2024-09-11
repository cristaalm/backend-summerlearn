from rest_framework import serializers
from accounts.models import Areas, Programs


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