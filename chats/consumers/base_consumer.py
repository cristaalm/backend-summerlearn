import json
import jwt
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from asgiref.sync import sync_to_async
from .message_handlers import handle_start_chats, handle_init_messages, handle_start_contacts, handle_send_message, handle_typing, handle_seen, handle_is_online

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        
        # Añadir al usuario al grupo general
        await self.channel_layer.group_add("general", self.channel_name)

    async def disconnect(self, close_code):
        # Enviar mensaje de desconexión al grupo general si el usuario está autenticado
        if hasattr(self, 'user_id'):
            await self.channel_layer.group_send(
                "general",
                {
                    'type': 'status',
                    'content': {'id': self.user_id, 'status': False}
                }
            )
            await handle_is_online(self, {'status': False})
        
        # Remover del grupo del usuario y del grupo general
        if hasattr(self, 'user_group_name'):
            await self.channel_layer.group_discard(self.user_group_name, self.channel_name)
        await self.channel_layer.group_discard("general", self.channel_name)

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')
            token = text_data_json.get('token')
            refresh_token = text_data_json.get('refresh_token')
            content = text_data_json.get('content', {})
        except KeyError:
            await self.send(json.dumps({
                'type': 'critical_error',
                'content': {'error': 'Mensaje inválido', 'console': 'Error en los datos'}
            }))
            return

        try:
            if token is None:
                raise ValueError('No se encontró el token')
            # Decodificación del token de acceso
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            self.user_id = str(payload['user_id'])
            self.user_rol = str(payload['rol'])
        except jwt.ExpiredSignatureError:
            # Token expirado, intenta refrescarlo
            if refresh_token:
                try:
                    # Llamada sincrónica envuelta en database_sync_to_async
                    new_access_token = await sync_to_async(self.refresh_access_token)(refresh_token)
                    self.user_id = await sync_to_async(self.get_user_id_from_token)(new_access_token)

                    # Enviar nuevo token al cliente
                    await self.send(json.dumps({
                        'type': 'token_refreshed',
                        'content': {'new_access_token': new_access_token}
                    }))
                except jwt.InvalidTokenError:
                    await self.send(json.dumps({
                        'type': 'critical_error',
                        'content': {'error': 'Token de refresco inválido'}
                    }))
                    return
            else:
                await self.send(json.dumps({
                    'type': 'critical_error',
                    'content': {'error': 'El token ha expirado y no se proporcionó un token de refresco'}
                }))
                return
        except (jwt.InvalidTokenError, KeyError, ValueError):
            await self.send(json.dumps({
                'type': 'critical_error',
                'content': {'error': 'Credenciales inválidas'}
            }))
            return

        self.user_group_name = f'user_{self.user_id}'
        await self.channel_layer.group_add(self.user_group_name, self.channel_name)

        # Lógica para manejar los mensajes según el tipo
        if message_type == "start_chats":
            # Enviar mensaje al grupo general de que el usuario se ha conectado
            await self.channel_layer.group_send(
                "general",
                {
                    'type': 'status',
                    'content': {'id': self.user_id, 'status': True}
                }
            )
            await handle_start_chats(self)
            await handle_is_online(self, {'status': True})
        elif message_type == "start_messages":
            await handle_init_messages(self)
        elif message_type == "start_contacts":
            await handle_start_contacts(self)
        elif message_type == "send_message":
            if hasattr(self, 'user_id'):
                await handle_send_message(self, content)
            else:
                await self.send(json.dumps({
                    'type': 'critical_error',
                    'content': {'error': 'Usuario no autenticado'}
                }))
        elif message_type == "ping":
            pass
        elif message_type == "typing":
            if hasattr(self, 'user_id'):
                await handle_typing(self, content)
        elif message_type == "seen":
            if hasattr(self, 'user_id'):
                await handle_seen(self, content)
        else:
            await self.send(json.dumps({
                'type': 'critical_error',
                'content': {'error': 'Tipo de mensaje desconocido'}
            }))

    # Esta función envuelve la lógica de refrescar el token de acceso
    def refresh_access_token(self, refresh_token):
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken(refresh_token)
        return str(refresh.access_token)

    # Esta función obtiene el user_id del nuevo token
    def get_user_id_from_token(self, token):
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return str(payload['user_id'])

    async def chat_message(self, event):
        content = event['content']
        await self.send(text_data=json.dumps({
            'type': 'success',
            'content': content
        }))

    async def message_received(self, event):
        content = event['content']
        await self.send(text_data=json.dumps({
            'type': 'message_received',
            'content': content
        }))

    async def message_sent(self, event):
        content = event['content']
        await self.send(text_data=json.dumps({
            'type': 'message_sent',
            'content': content
        }))

    async def typing(self, event):
        content = event['content']
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'content': content
        }))

    async def status(self, event):
        content = event['content']
        await self.send(text_data=json.dumps({
            'type': 'status',
            'content': content
        }))