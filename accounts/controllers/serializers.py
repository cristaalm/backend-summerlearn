from rest_framework import serializers
from accounts.models import Users, Status, Rol
from django.contrib.auth.hashers import make_password


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
        read_only_fields = ('users_id',)

    def create(self, validated_data):
        # Almacena la contraseña en texto claro
        return super().create(validated_data)





# Define un serializer basado en el modelo 'Status'.
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status  # Define el modelo que será serializado.

        fields = '__all__'
        # Lista los campos del modelo 'User' que serán serializados.

        read_only_fields = ('status_id',)

class RolSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Rol

        fields = '__all__'

        read_only_fields = ('rol_id',)