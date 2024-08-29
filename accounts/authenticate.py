from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Users
from accounts.controllers.serializers import UsersSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model



@api_view(['POST'])
def register_user(request):

    serializer = UsersSerializer(data=request.data)

    if serializer.is_valid():

        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

####################################################################################################



@api_view(['POST'])
def login_user(request):
    email = request.data.get('users_mail')
    password = request.data.get('users_password')

    try:
        # Obtener el usuario de la base de datos
        user = Users.objects.get(users_mail=email)
        
        # Verificar la contraseña (esto debe estar bien implementado para la seguridad)
        if user.users_password == password:  # Comparación simple (debe ser hash en producción)
            # Generar token JWT
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    except Users.DoesNotExist:
        return Response({'detail': 'User does not exist'}, status=status.HTTP_401_UNAUTHORIZED)