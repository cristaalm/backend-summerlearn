from .controllers.serializers import UsersSerializer

########################################################################################
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenRefreshView
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

    @action(detail=False, methods=['post'], url_path='refresh-token')
    def refresh_token(self, request):
        """
        Acción personalizada para refrescar el token de acceso.
        Requiere el token de refresh como dato de entrada.
        """
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({'detail': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Intenta generar un nuevo token de acceso a partir del token de refresh
            refresh = RefreshToken(refresh_token)
            return Response({
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)