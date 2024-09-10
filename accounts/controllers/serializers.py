from rest_framework import serializers
from accounts.models import UserData, Status, Rol
from django.contrib.auth.hashers import make_password


########################################################################################
# Define un serializer basado en el modelo 'UserData'.
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = '__all__'
        read_only_fields = ('id',)


########################################################################################
# Define un serializer basado en el modelo 'UserData'.
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = UserData
        fields = ['name', 'first_name','last_name','email', 'password', 'users_photo', 'users_birthdate', 'users_phone', 'users_rol', 'users_status', 'users_tour']
    
    def create(self, validated_data):
        # Extract the password from validated data
        password = validated_data.pop('password')
        
        # Create the user with the rest of the validated data
        user = UserData(**validated_data)
        
        # Hash the password
        user.password = make_password(password)
        
        # Save the user
        user.save()
        
        return user


########################################################################################

# Define un serializer basado en el modelo 'Status'.
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status  # Define el modelo que será serializado.

        fields = '__all__'
        # Lista los campos del modelo 'User' que serán serializados.

        read_only_fields = ('status_id',)


########################################################################################
# Define un serializer basado en el modelo 'Rol'.
class RolSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Rol

        fields = '__all__'

        read_only_fields = ('rol_id',)