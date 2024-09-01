from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Users
from .controllers.serializers import UsersSerializer
from rest_framework import permissions

############################################################################################################


class Authenticate(viewsets.ModelViewSet):
    # Define el queryset que será usado por este ViewSet.
    queryset = Users.objects.all()
    # Define el serializador que se usará para transformar datos entre los modelos y JSON.
    serializer_class = UsersSerializer
    # Define las clases de permiso que permiten el acceso a cualquier usuario (sin autenticación).
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'], url_path='register')
    def register_user(self, request):
        """
        Acción personalizada para registrar un nuevo usuario.
        - Se usa el método POST.
        - Se espera recibir datos del usuario en el request.
        - Se valida y guarda el nuevo usuario.
        - Se genera un token de autenticación JWT para el usuario registrado.
        """
        # Crea un nuevo serializador con los datos recibidos en la solicitud.
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            # Si los datos del serializador son válidos, guarda el nuevo usuario.
            user = serializer.save()
            # Genera un token de acceso JWT para el usuario recién registrado.
            refresh = RefreshToken.for_user(user)
            # Retorna el token de acceso y de actualización en la respuesta con el estado HTTP 201 Created.
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        
        # Si los datos del serializador no son válidos, retorna los errores en la respuesta con el estado HTTP 400 Bad Request.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='login')
    def login_user(self, request):
        """
        Acción personalizada para iniciar sesión de un usuario.
        - Se usa el método POST.
        - Se espera recibir correo electrónico y contraseña en el request.
        - Se valida el usuario y la contraseña.
        - Se genera un token de autenticación JWT para el usuario autenticado.
        """
        # Obtiene el correo electrónico y la contraseña del request.
        email = request.data.get('users_mail')
        password = request.data.get('users_password')

        try:
            # Intenta obtener el usuario con el correo electrónico proporcionado.
            user = Users.objects.get(users_mail=email)
            
            # Verifica la contraseña (debe ser hash en producción para mayor seguridad).
            if user.users_password == password:
                # Si la contraseña es correcta, genera un token de acceso JWT.
                refresh = RefreshToken.for_user(user)
                # Retorna el token de acceso y de actualización en la respuesta con el estado HTTP 200 OK.
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            
            # Si la contraseña es incorrecta, retorna un mensaje de error con el estado HTTP 401 Unauthorized.
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        except Users.DoesNotExist:
            # Si el usuario no existe, retorna un mensaje de error con el estado HTTP 401 Unauthorized.
            return Response({'detail': 'User does not exist'}, status=status.HTTP_401_UNAUTHORIZED)