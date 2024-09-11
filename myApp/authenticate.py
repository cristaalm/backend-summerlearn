from .controllers.serializers import UsersSerializer

########################################################################################
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
########################################################################################

# Define la clase 'Authenticate' que hereda de 'viewsets.ViewSet'.
class Authenticate(viewsets.ViewSet):
    # Define el serializador que se usará para transformar datos entre los modelos y JSON.
    serializer_class = UsersSerializer

    @action(detail=False, methods=['post'], url_path='register')
    def register_user(self, request):
        """
        Acción personalizada para registrar un nuevo usuario.
        """
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
