from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
# from .models import Users
from .controllers.serializers import UsersSerializer


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

    @action(detail=False, methods=['post'], url_path='login')
    def login_user(self, request):
        """
        Acción personalizada para iniciar sesión de un usuario.
        """
        email = request.data.get('users_mail')
        password = request.data.get('users_password')

        try:
            user = Users.objects.get(users_mail=email)
            # Verifica la contraseña (asegúrate de usar un método de hash en producción).
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Users.DoesNotExist:
            return Response({'detail': 'User does not exist'}, status=status.HTTP_401_UNAUTHORIZED)
