from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from myApp.models import UserData
from .keys import create_temp_key
from myApp.settings import EMAIL_HOST_USER

@csrf_exempt  # Desactivar CSRF solo para pruebas, no recomendado en producción
def send_email_view(request):
    if request.method == 'POST':
        try:
            # Convertir el cuerpo de la solicitud de JSON a un diccionario
            data = json.loads(request.body)
            email = data.get('email', None)

            if email is None:
                return JsonResponse({'error': 'Correeo electrónico no proporcionado.'}, status=400)

            # Buscar el usuario por correo electrónico
            try:
                user = UserData.objects.get(email=email)  # Asegúrate de que el usuario existe
            except UserData.DoesNotExist:
                return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

            # Generar la clave temporal y el enlace de restablecimiento
            key = create_temp_key(user.id, expiration_time=600)  
            reset_link = f'http://localhost:5173/reset-password/{key}/'  

            # Renderizar el contenido del correo desde una plantilla
            html_content = render_to_string('mail.min.html', {'nombre': user.name, 'reset_link': reset_link})
            text_content = 'Este es el contenido del correo en texto plano.'

            # Crear el mensaje
            subject = 'Recuperación de contraseña'
            from_email = EMAIL_HOST_USER
            to = [email]  

            email_message = EmailMultiAlternatives(subject, text_content, from_email, to)
            email_message.attach_alternative(html_content, "text/html")

            # Enviar el correo
            email_message.send()
            return JsonResponse({'message': 'Correo enviado exitosamente.'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Datos inválidos. Se esperaba un JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido.'}, status=405)

@csrf_exempt
def send_mail_accepted(data):
    try:
        # Convertir el cuerpo de la solicitud de JSON a un diccionario
        email = data.get('email', None)
        name = data.get('name', None)

        if email is None or name is None:
            return JsonResponse({'error': 'Faltan datos en la solicitud.'}, status=400)

        # Renderizar el contenido del correo desde una plantilla
        html_content = render_to_string('mail_accepted.html', {'nombre': name})
        text_content = 'Este es el contenido del correo en texto plano.'

        # Crear el mensaje
        subject = 'Estado de solicitud'
        from_email = EMAIL_HOST_USER
        to = [email]  

        email_message = EmailMultiAlternatives(subject, text_content, from_email, to)
        email_message.attach_alternative(html_content, "text/html")

        # Enviar el correo
        email_message.send()
        return JsonResponse({'message': 'Correo enviado exitosamente.'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt
def send_mail_rejected(data):
    try:
        # Convertir el cuerpo de la solicitud de JSON a un diccionario
        email = data.get('email', None)
        name = data.get('name', None)

        if email is None or name is None:
            return JsonResponse({'error': 'Faltan datos en la solicitud.'}, status=400)

        # Renderizar el contenido del correo desde una plantilla
        html_content = render_to_string('mail_rejected.html', {'nombre': name})
        text_content = 'Este es el contenido del correo en texto plano.'

        # Crear el mensaje
        subject = 'Estado de solicitud'
        from_email = EMAIL_HOST_USER
        to = [email]  

        email_message = EmailMultiAlternatives(subject, text_content, from_email, to)
        email_message.attach_alternative(html_content, "text/html")

        # Enviar el correo
        email_message.send()
        return JsonResponse({'message': 'Correo enviado exitosamente.'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)