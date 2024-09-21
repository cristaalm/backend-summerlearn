from .controllers.serializers import RolSeralizer, StatusSerializer, UsersSerializer, RegisterSerializer
from myApp.models import Rol, Status, UserData
from django.db import IntegrityError


########################################################################################
# Importaciones de Django REST Framework
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny  
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
########################################################################################

class RegisterView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to access the registration endpoint

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Save the user, ensuring unique constraints are handled
                user = serializer.save()
                
                # Generate JWT refresh and access tokens
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_201_CREATED)
            
            except IntegrityError:
                # Handle cases where unique fields (e.g., name, email) violate the constraints
                return Response({
                    "error": "A user with this information already exists."
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Return any serializer validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

########################################################################################

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserData.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # Custom action to filter users by id_rol
    @action(detail=False, methods=['get'], url_path='by-id-rol')
    def getByRol(self, request):
        id_rol = request.query_params.get('id_rol', None)
        if id_rol:
            # Filtra y selecciona solo los campos 'id' y 'name'
            users_by_rol = UserData.objects.filter(users_rol=id_rol).values('id', 'name')
            return Response(users_by_rol)  # Ya no es necesario usar el serializer, ya que solo devuelves campos seleccionados
        else:
            return Response({'error': 'id_rol no proporcionado'}, status=400)

########################################################################################

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [permissions.AllowAny]
    

########################################################################################

class RolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSeralizer
    permission_classes = [permissions.AllowAny]