# path: chats/consumers.py

import json
from datetime import datetime
import jwt
import uuid
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from pytz import timezone
from asgiref.sync import sync_to_async
from urllib.parse import parse_qs

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extraer token del query string
        try:
            query_string = self.scope['query_string'].decode('utf-8')
            query_params = parse_qs(query_string)
            
            token = query_params.get('token', [None])[0]  # Extraer el token
            
            if token is None:
                raise ValueError('No se encontró el token')

            # Decodificar el token JWT
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            self.user_id = str(payload['user_id'])

        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, KeyError, ValueError):
            await self.close()
            return

        # Crear un grupo único para el usuario
        self.user_group_name = f'user_{self.user_id}'

        # Unirse al grupo de usuario
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo de usuario
        if hasattr(self, 'user_group_name'):
            await self.channel_layer.group_discard(
                self.user_group_name,
                self.channel_name
            )

    # Recibir mensaje de WebSocket
    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')
            content = text_data_json.get('content', {})
        except KeyError:
            # Manejar error de estructura de datos
            await self.send(json.dumps({'type': 'critical_error', 'content': {'error': 'Mensaje inválido', 'console': 'Error en los datos'}}))
            return

        # Enviar a la función correspondiente basada en el "type"
        if message_type == "start":
            await self.handle_start()
        elif message_type == "send_message":
            if hasattr(self, 'user_id'):  # Verificar si el usuario ya está autenticado
                await self.handle_send_message(content)
            else:
                await self.send(json.dumps({'type': 'critical_error', 'content': {'error': 'Usuario no autenticado'}}))
        elif message_type == "ping":
            await self.send(json.dumps({'type': 'pong'}))
        elif message_type == "typing":
            if hasattr(self, 'user_id'):
                await self.handle_typing(content)
        else:
            await self.send(json.dumps({'type': 'critical_error', 'content': {'error': 'Tipo de mensaje desconocido'}}))

    async def handle_typing(self, content):
        try: 
            recipient_id = content['recipient_id']
            isTyping = content['isTyping']
            chat_id = f'{min(int(self.user_id), int(recipient_id))}_{max(int(self.user_id), int(recipient_id))}'
            recipient_group_name = f'user_{recipient_id}'
        except KeyError:
            await self.send(json.dumps({'type': 'critical_error', 'content': {'error': 'Datos incompletos'}}))
            return

        # Enviar mensaje al grupo del destinatario
        await self.channel_layer.group_send(
            recipient_group_name,
            {
                'type': 'typing',
                'content': {'id': chat_id, 'isTyping': isTyping}
            }
        )

    async def handle_start(self):
        # Obtener el ID del usuario desde el token
        user_id = self.user_id

        # Recuperar los chats del usuario de forma asíncrona
        chats = await sync_to_async(self.get_init_chats)(user_id)

        # Enviar la información de los chats al cliente
        await self.send(json.dumps({
            'type': 'init_chats',
            'content': chats
        }))
        
        messages = await sync_to_async(self.get_init_messages)(user_id, chats)

        # Enviar la información de los mensajes al cliente
        await self.send(json.dumps({
            'type': 'init_messages',
            'content': messages
        }))


    def get_init_messages(self, user_id, chats):
        from myApp.models import Messages
        messages_data_list = []

        for chat_data in chats:
            chat_id = chat_data['id']

            # Obtener los mensajes del chat
            messages = Messages.objects.filter(messages_chat=chat_id).order_by('messages_date')

            for message in messages:
                # Crear el diccionario de datos del mensaje
                message_data = {
                    'id': message.messages_id,
                    'message': message.messages_content,
                    'date': message.messages_date.isoformat(),
                    'user': message.messages_user.id,
                    'chat': message.messages_chat.chat_id
                }


                # Añadir a la lista
                messages_data_list.append(message_data)

        return messages_data_list
        

    def get_init_chats(self, user_id):
        from myApp.models import Chat, Messages, UserData
        user = UserData.objects.get(id=user_id)
        chats = Chat.objects.filter(chat_user1=user) | Chat.objects.filter(chat_user2=user)

        chat_data_list = []
        for chat in chats:
            chat_user = None
            if str(chat.chat_user1.id) == str(user_id):
                chat_user = UserData.objects.get(id=str(chat.chat_user2.id))
            
            elif str(chat.chat_user2.id) == str(user_id):
                chat_user = UserData.objects.get(id=str(chat.chat_user1.id))

            if not chat_user:
                continue

            # Obtener el último mensaje del chat
            last_message = Messages.objects.filter(messages_chat=chat).order_by('-messages_date').first()
            last_message_data = None
            if last_message:
                last_message_data = {
                    'id': last_message.messages_id,
                    'content': last_message.messages_content,
                    'date': last_message.messages_date.isoformat()
                }

            # Crear el diccionario de datos del chat
            chat_data = {
                'id': chat.chat_id,
                'date': chat.chat_date.isoformat(),
                'user': {
                    'id': chat_user.id,
                    'name': chat_user.name,
                    'email': chat_user.email,
                    'userPhoto': chat_user.users_photo,
                    'rol': chat_user.users_rol.rol_name
                },
                'lastMessage': last_message_data
            }

            # Añadir a la lista
            chat_data_list.append(chat_data)

        return chat_data_list
    
    def get_chat(self, chat_id):
        from myApp.models import Chat
        return Chat.objects.filter(chat_id=chat_id).first()

    def create_chat(self, chat_id, user1_id, user2_id):
        from myApp.models import UserData, Chat
        return Chat.objects.create(chat_id=chat_id, chat_date=datetime.now(timezone('America/Mexico_City')), chat_user1=UserData.objects.get(id=user1_id), chat_user2=UserData.objects.get(id=user2_id))

    def create_message(self, message_id, message, date, user_id, chat_id):
        from myApp.models import UserData, Chat, Messages
        return Messages.objects.create(messages_id=message_id, messages_content=message, messages_date=date, messages_user=UserData.objects.get(id=user_id), messages_chat=Chat.objects.get(chat_id=chat_id))

    def serialize_chat(self, chat, recipient_id, message_id, message, date):
        user1 = chat.chat_user1
        user2 = chat.chat_user2
        user_recipient = user1 if user1.id == recipient_id else user2

        # Serializar chat
        chat_data = {
            'chat_id': chat.chat_id,
            'chat_date': chat.chat_date.isoformat(),
            'chat_user': {
                'id': user_recipient.id,
                'name': user_recipient.name,
                'email': user_recipient.email,
                'users_photo': user_recipient.users_photo,
                'rol_name': user_recipient.users_rol.rol_name
            },
            'lastMessage': {
                'id': message_id,
                'content': message,
                'date': date
            }
        }

        return chat_data

    async def handle_send_message(self, content):
        # * Generar un id único para el mensaje * #
        message_id = str(uuid.uuid4())

        try:  # ? Comprobar si los datos son enviados correctamente ? #
            message = content['message']
            recipient_id = content['recipient_id']
            date = content['date']
        except KeyError:  # ! Error de datos incompletos ! #
            await self.send(json.dumps({'type': 'critical_error', 'content': {'error': 'Datos incompletos'}}))
            return

        # ? Verificar que la fecha ya venía en formato ISO ? #
        try:
            datetime.fromisoformat(date)
        except ValueError:  # ! Error de formato de fecha ! #
            await self.send(json.dumps({'type': 'critical_error', 'content': {'error': 'Formato de fecha inválido'}}))
            return

        # ? Verificar si el destinatario está conectado ? #
        recipient_group_name = f'user_{recipient_id}'

        # Obtener o crear el chat
        chat_id = f'{min(int(self.user_id), int(recipient_id))}_{max(int(self.user_id), int(recipient_id))}'
        chat =  await sync_to_async(self.get_chat)(chat_id)
        if not chat:
            chat =  await sync_to_async(self.create_chat)(chat_id, self.user_id, recipient_id)
            if not chat:  # ! Error al crear el chat ! #
                await self.send(json.dumps({'type': 'critical_error', 'content': {'error': 'Error al crear el chat'}}))
                return

        # Guardar el mensaje en la base de datos
        Message = await sync_to_async(self.create_message)(message_id, message, date, self.user_id, chat_id)
        if not Message:  # ! Error al guardar el mensaje ! #
            await self.send(json.dumps({'type': 'critical_error', 'content': {'error': 'Error al enviar el mensaje'}}))
            return
        
        # Serializar chat
        chat_data = await sync_to_async(self.serialize_chat)(chat, recipient_id, message_id, message, date)

        # Enviar mensaje al grupo del destinatario y al emisor
        content = {'id': message_id, 'message': message, 'date': date, 'user': self.user_id, 'chat': chat_data}
        await self.channel_layer.group_send(
            recipient_group_name,
            {
                'type': 'message_received',
                'content': content
            }
        )

        # Enviar mensaje al grupo del emisor
        content = {'id': message_id, 'message': message, 'date': date, 'user': self.user_id, 'chat': chat_data}
        await self.channel_layer.group_send(
            self.user_group_name,
            {
                'type': 'message_sent',
                'content': content
            }
        )

    # Recibir mensaje del grupo de usuario 
    async def chat_message(self, event):
        content = event['content']

        # Enviar mensaje al WebSocket
        await self.send(text_data=json.dumps({
            'type': 'success',
            'content': content
        }))

    async def message_received(self, event):
        content = event['content']

        # Enviar el mensaje al WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message_received',
            'content': content
        }))

    async def message_sent(self, event):
        content = event['content']

        # Enviar el mensaje al WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message_sent',
            'content': content
        }))

    async def typing(self, event):
        content = event['content']

        # Enviar el mensaje al WebSocket
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'content': content
        }))