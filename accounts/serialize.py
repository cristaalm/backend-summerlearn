from rest_framework import serializers
from .models import Users, Status, Rol

# Define un serializer basado en el modelo 'User'.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users  # Define el modelo que será serializado.

        fields = ('users_id','users_name', 'users_photo', 'users_birthdate', 'users_mail',
                  'users_password', 'users_phone', 'users_rol', 'users_status', 'users_tour')
        # Lista los campos del modelo 'User' que serán serializados.

        read_only_fields = ('users_id',)

# Define un serializer basado en el modelo 'Status'.
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status  # Define el modelo que será serializado.

        fields = ('status_id', 'status_name')
        # Lista los campos del modelo 'User' que serán serializados.

        read_only_fields = ('status_id',)

class RolSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Rol

        fields = ('rol_id', 'rol_name')

        read_only_fields = ('rol_id',)