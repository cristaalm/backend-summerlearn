from .controllers.serializers import MyTokenObtainPairSerializer, RolSeralizer, StatusSerializer, UsersSerializer, RegisterSerializer, DecryptSerializer, decrypt
from myApp.models import Rol, Status, UserData
from django.core.files.storage import default_storage
from django.db import IntegrityError
from myApp.settings import MEDIA_ROOT
import os
import uuid

# Importar las funciones de envío de correos desde el archivo send_mail.py
from myApp.mails.send_mail import send_mail_accepted, send_mail_rejected

# ? ######################################################################################## ? #
# Importaciones de Django REST Framework
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny  
from rest_framework import status
from rest_framework import permissions
from rest_framework.reverse import reverse 
from rest_framework_simplejwt.views import TokenObtainPairView
# ? ######################################################################################## ? #

# ? ######################################################################################## ? #

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = UserData.objects.get(email=request.data['email'])
            if user.users_status.status_id == 1:
                return super().post(request, *args, **kwargs)
            else:
                return Response({'error': 'User is not active'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DecryptView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = DecryptSerializer(data=request.data)
        if serializer.is_valid():
            encrypted_text = serializer.validated_data['encrypted_text']
            try:
                decrypted_text = decrypt(encrypted_text, "cuatro_veinte")  # Call the decrypt function
                return Response({'decrypted_text': decrypted_text}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # validamos si el request es de tipo multipart/form-data
        if request.content_type !=  'application/json':
            # Manejar la imagen # Extraer la imagen del request
            users_photo = request.data.get('users_photo', None)

            if isinstance(users_photo, str) != True and users_photo and hasattr(users_photo, 'read'):
                # Caso FormData: Subir el archivo a un directorio y guardar la ruta
                filename = f"{uuid.uuid4()}.jpg"  # Generar nombre único
                path = os.path.join('usersImages', filename)
                default_storage.save(path, users_photo)  # Aquí 'users_photo' debe ser un archivo
                request.data['users_photo'] = f'media/usersImages/{filename}'

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = serializer.save()

                # En lugar de generar el token manualmente, usamos el serializer de MyTokenObtainPairSerializer
                token_serializer = MyTokenObtainPairSerializer(data={
                    'username': user.username,  # Usa el campo username del usuario
                    'email': user.email,  # El email enviado en el request
                    'status': user.users_status.status_id,  # El status del usuario
                    'password': request.data.get('password')  # El password enviado en el request
                })

                if token_serializer.is_valid():
                    return Response(token_serializer.validated_data, status=status.HTTP_201_CREATED)
                else:
                    return Response(token_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except IntegrityError:
                return Response({"error": "A user with this information already exists."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# ? ######################################################################################## ? #

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserData.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # Custom action to filter users by id_rol
    @action(detail=False, methods=['get'], url_path='by-id-rol')
    def get_by_rol(self, request):
        id_rol = request.query_params.get('id_rol')
        if not id_rol:
            return Response({'error': 'id_rol is required'}, status=HTTP_400_BAD_REQUEST)
        
        # Filter users by role ID and select only specific fields
        users_by_rol = UserData.objects.filter(users_rol=id_rol).values('id', 'name', 'email')
        return Response(users_by_rol)

    # Custom action to filter users by id_status
    @action(detail=False, methods=['get'], url_path='by-status')
    def get_by_status(self, request):
        id_status = request.query_params.get('id_status')
        if not id_status:
            return Response({'error': 'id_status is required'}, status=HTTP_400_BAD_REQUEST)
        
        # Filter users by status and exclude those with role 3
        users_by_status = UserData.objects.filter(users_status=id_status).exclude(users_rol=3).values(
            'id', 'users_photo', 'name', 'email', 'users_rol__rol_name', 'users_status__status_name'
        )
        return Response(users_by_status)

    # Custom action to filter users with status 1 and 2
    @action(detail=False, methods=['get'], url_path='show-by-status')
    def show_by_status(self, request):
        # Filter users whose status is 1 or 2
        users_by_status = UserData.objects.filter(users_status__in=[1, 2, 4])
        
        # Use the serializer to return all fields for these users
        serializer = self.get_serializer(users_by_status, many=True)
        return Response(serializer.data)

    # Custom action to update user status by id_status
    @action(detail=False, methods=['post'], url_path='update-status')
    def update_status(self, request):
        user_id = request.data.get('id')
        new_status_id = request.data.get('id_status')
        
        if not user_id or not new_status_id:
            return Response({'error': 'Both id and id_status are required'}, status=HTTP_400_BAD_REQUEST)
        
        try:
            # Find the user by ID
            user = UserData.objects.get(id=user_id)

            # verificamos si el anterior estado es igual a 3 (pendiente) o 4 (rechazado)
            if user.users_status.status_id == 3 or user.users_status.status_id == 4:

                data = {
                    'email': user.email,
                    'name': user.name
                }

                # si el nuevo estado es 1 (activo), enviamos un correo de aceptación
                if new_status_id == 1: 
                    send_mail_accepted(data)
                # si el nuevo estado es 2 (rechazado), enviamos un correo de rechazo
                elif new_status_id == 4:
                    send_mail_rejected(data)
                
            
            # Update the user's status
            user.users_status_id = new_status_id
            user.save()
            
            # Return a success message along with the updated user data
            serializer = self.get_serializer(user)
            return Response({'success': 'User status updated successfully', 'user': serializer.data})
        except UserData.DoesNotExist:
            return Response({'error': 'User not found'}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)
        
    # Acción custom para actualizar la imagen del usuario
    @action(detail=False, methods=['post'], url_path='update-photo')
    def update_photo(self, request):
        user_id = request.data.get('id')
        users_photo = request.data.get('users_photo')
        
        if not user_id or not users_photo:
            return Response({'error': 'Both id and users_photo are required'}, status=HTTP_400_BAD_REQUEST)
        
        try:
            # Find the user by ID
            user = UserData.objects.get(id=user_id)
            
            # extraemos la extensión de la imagen
            ext = users_photo.name.split('.')[-1]

            # Generar un nombre único para la imagen
            filename = f'{uuid.uuid4()}.{ext}'
            path = os.path.join('usersImages', filename)
            
            # Guardar la imagen en el directorio
            default_storage.save(path, users_photo)
            
            # Eliminar la imagen anterior si existe y no es la imagen por defecto
            if user.users_photo and user.users_photo != 'media/usersImages/placeholderUser.jpg':
                # removemos /media/ de la ruta de la imagen
                old_path = os.path.join(MEDIA_ROOT, user.users_photo.replace('media/', ''))
                # eliminamos y comprobamos si se eliminó correctamente
                if os.path.exists(old_path):
                    os.remove(old_path)
                    if os.path.exists(old_path):
                        return Response({'error': 'Failed to delete old image'}, status=HTTP_400_BAD_REQUEST)
                
            
            # Actualizar la ruta de la imagen en la base de datos
            user.users_photo = f'media/usersImages/{filename}'
            user.save()
            
            # Retornar un mensaje de éxito y la ruta de la imagen
            return Response({'success': 'User photo updated successfully', 'photo': user.users_photo})
        except UserData.DoesNotExist:
            return Response({'error': 'User not found'}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)

    # Custom action para actualizar la contraseña del usuario
    @action(detail=False, methods=['post'], url_path='changePassword')
    def change_password(self, request):
        user_id = request.data.get('id')
        new_password = request.data.get('newPassword')
        current_password = request.data.get('currentPassword')

        if not user_id or not new_password:
            return Response({'error': 'Both id and password are required', 'spanishError': 'Por favor, llene todos los campos'}, status=HTTP_400_BAD_REQUEST)
        
        try:
            # Find the user by ID
            user = UserData.objects.get(id=user_id)
            
            # Verificar la contraseña actual
            if not user.check_password(current_password):
                return Response({'error': 'Current password is incorrect', 'spanishError': 'La contraseña actual es incorrecta'}, status=HTTP_400_BAD_REQUEST)
            0
            # Actualizar la contraseña del usuario
            user.set_password(new_password)
            user.save()
            
            # Retornar un mensaje de éxito
            return Response({'success': 'User password updated successfully', 'spanishSuccess': 'Contraseña actualizada correctamente'})
        except UserData.DoesNotExist:
            return Response({'error': 'User not found', 'spanishError': 'Usuario no encontrado'}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)
        
    # Custom action para obtener la imagen del usuario
    @action(detail=False, methods=['get'], url_path='get-photo')
    def get_photo(self, request):
        user_id = request.query_params.get('id')
        
        if not user_id:
            return Response({'error': 'id is required'}, status=HTTP_400_BAD_REQUEST)
        
        try:
            # Find the user by ID
            user = UserData.objects.get(id=user_id)
            
            # Retornar la ruta de la imagen
            return Response({'photo': user.users_photo})
        except UserData.DoesNotExist:
            return Response({'error': 'User not found'}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)
        
    # Custom action to filter users by id_rol and id_status
    @action(detail=False, methods=['get'], url_path='by-rol-status')
    def get_by_rol_status(self, request):
        '''
        Filtra los usuarios por rol y estado, y cuenta cuántos usuarios hay en cada categoría.

        Returns:
            Response: Un diccionario con los resultados de la consulta.
        '''
        # Obtenemos todos los roles y estados
        roles = Rol.objects.all()
        status_activo = Status.objects.get(status_id=1)
        status_pendiente = Status.objects.get(status_id=3)
        
        # Inicializamos el diccionario de resultados
        result = {
            "Administrador": 0,
            "Coordinador": 0,
            "Donante": 0,
            "Voluntario": 0,
            "Beneficiario": 0,
            "Inactivo": 0,
            "Total": 0,
            "pendientes": False
        }

        # Contamos los usuarios activos por rol
        for rol in roles:
            rol_count = UserData.objects.filter(users_rol=rol.rol_id, users_status=status_activo.status_id).count()
            if rol.rol_id == 1:
                result["Administrador"] += rol_count
            elif rol.rol_id == 2:
                result["Coordinador"] += rol_count
            elif rol.rol_id == 3:
                result["Donante"] += rol_count
            elif rol.rol_id == 4:
                result["Voluntario"] += rol_count
            elif rol.rol_id == 5:
                result["Beneficiario"] += rol_count
            result["Total"] += rol_count
        
        # Contamos todos los usuarios inactivos (usuarios con cualquier estado que no sea activo)
        inactivo_count = UserData.objects.exclude(users_status=status_activo.status_id).count()
        pendiente_count = UserData.objects.filter(users_status=status_pendiente.status_id).count()
        result["Inactivo"] += inactivo_count
        result["Total"] += inactivo_count

        if pendiente_count > 0:
            result["pendientes"] = True
        
        return Response(result)
        
# ? ######################################################################################## ? #

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

# ? ######################################################################################## ? #

class RolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSeralizer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
# ? ######################################################################################## ? #



# Custom APIVIEW para el API Root

class CustomAPIRootView(APIView):

    # Vista personalizada para el API Root. Añadir manualmente las URLs de las otras apps para que aparezcan en el API Root

    def get(self, request, *args, **kwargs):
        return Response({
            'users': reverse('users-list', request=request, format=kwargs.get('format')),
            'roles': reverse('rol-list', request=request, format=kwargs.get('format')),
            'statuses': reverse('status-list', request=request, format=kwargs.get('format')),
            'areas': reverse('areas-list', request=request, format=kwargs.get('format')),
            'programs': reverse('programs-list', request=request, format=kwargs.get('format')),
            'activities': reverse('activities-list', request=request, format=kwargs.get('format')),
            'days': reverse('days-list', request=request, format=kwargs.get('format')),
            'schedules': reverse('schedules-list', request=request, format=kwargs.get('format')),
            'donations': reverse('donations-list', request=request, format=kwargs.get('format')),
            'bills': reverse('bills-list', request=request, format=kwargs.get('format')),
            'children': reverse('childrens-list', request=request, format=kwargs.get('format')),
        })
