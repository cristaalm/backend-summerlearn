import random
import string
import time
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from myApp.models import UserData 
from django.shortcuts import render

# Diccionario para almacenar claves y su información
temp_keys = {}

def generate_random_key(length=10):
    """Genera una clave aleatoria de longitud específica."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length)) 

def create_temp_key(user_id, expiration_time):
    """Crea una clave temporal para un usuario."""
    key = generate_random_key()
    expire_at = time.time() + expiration_time 
    temp_keys[key] = {'user_id': user_id, 'expires_at': expire_at} 
    return key

@csrf_exempt  
def get_id_user(request):
    if request.method == 'POST':
        try:
            # Cargar los datos del cuerpo de la solicitud
            user_data = json.loads(request.body)
            email = user_data.get('email')  
            
            if not email:
                return JsonResponse({'error': 'El campo email es obligatorio'}, status=400)
            
            # Buscar el usuario por correo electrónico
            try:
                user = UserData.objects.get(email=email)  # Usar get para obtener un solo usuario
            except UserData.DoesNotExist:
                return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
            
            # Crear una clave temporal y almacenar el id del usuario
            key = create_temp_key(user.id, expiration_time=600)  # Clave válida por 120 segundos
            
            
            name = user.name  
            
           
            context = {
                'name': name,
                'key': key
            }
            
            # Renderizar la plantilla con el contexto
            return render(request, 'template/mail.min.html', context)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato de datos inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)  

    # Si el método no es POST
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# Vista para obtener datos del usuario con la key temporal
@csrf_exempt
def update_password_by_key(request, key):
    if request.method == 'PATCH':
        try:
            # Verificar si la key existe en el diccionario y si no ha expirado
            key_data = temp_keys.get(key)
            
            if not key_data:
                return JsonResponse({'error': 'Key no válida o expirada'}, status=404)
            
            # Verificar si la key ha expirado
            if time.time() > key_data['expires_at']:
                del temp_keys[key]
                return JsonResponse({'error': 'Key expirada'}, status=403)
            
            # Obtener el ID del usuario a partir de la key
            user_id = key_data['user_id']
            user = UserData.objects.get(id=user_id)

            # Obtener la nueva contraseña del cuerpo de la solicitud
            data = json.loads(request.body)
            new_password = data.get('password')

            # Validar la nueva contraseña
            if not new_password:
                return JsonResponse({'error': 'Nueva contraseña no proporcionada'}, status=400)

            # Actualizar la contraseña del usuario
            user.set_password(new_password)  # Usa este método para cifrar la contraseña
            user.save()

            return JsonResponse({'message': 'Contraseña actualizada con éxito'}, status=200)

        except UserData.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)