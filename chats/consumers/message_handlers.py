import uuid
import json
from datetime import datetime
from asgiref.sync import sync_to_async
from .utils import get_init_chats, get_init_messages, change_seen, get_chat, create_chat, create_message, serialize_chat


async def handle_start(self):
    user_id = self.user_id
    chats = await sync_to_async(get_init_chats)(user_id)
    await self.send(json.dumps({
        'type': 'init_chats',
        'content': chats
    }))

    messages = await sync_to_async(get_init_messages)(user_id, chats)
    await self.send(json.dumps({
        'type': 'init_messages',
        'content': messages
    }))


async def handle_send_message(self, content):
    message_id = str(uuid.uuid4())
    try:
        message = content['message']
        recipient_id = content['recipient_id']
        date = content['date']
    except KeyError:
        await self.send(json.dumps({
            'type': 'critical_error', 
            'content': {'error': 'Datos incompletos'}
        }))
        return

    try:
        datetime.fromisoformat(date)
    except ValueError:
        await self.send(json.dumps({
            'type': 'critical_error', 
            'content': {'error': 'Formato de fecha inválido'}
        }))
        return

    recipient_group_name = f'user_{recipient_id}'
    chat_id = f'{min(int(self.user_id), int(recipient_id))}_{max(int(self.user_id), int(recipient_id))}'

    chat = await sync_to_async(get_chat)(chat_id)
    if not chat:
        chat = await sync_to_async(create_chat)(chat_id, self.user_id, recipient_id)
        if not chat:
            await self.send(json.dumps({
                'type': 'critical_error', 
                'content': {'error': 'Error al crear el chat'}
            }))
            return
    else:
        chat_user1_id = await sync_to_async(lambda: chat.chat_user1.id)()
        if str(chat_user1_id) == str(self.user_id):
            chat.chat_seen_user2 = False
            chat.chat_seen_user1 = True
        else:
            chat.chat_seen_user1 = False
            chat.chat_seen_user2 = True
        await sync_to_async(chat.save)()

    Message = await sync_to_async(create_message)(message_id, message, date, self.user_id, chat_id)
    if not Message:
        await self.send(json.dumps({
            'type': 'critical_error', 
            'content': {'error': 'Error al enviar el mensaje'}
        }))
        return

    chat_data = await sync_to_async(serialize_chat)(chat, recipient_id, message_id, message, date)
    content = {'id': message_id, 'message': message, 'date': date, 'user': self.user_id, 'chat': chat_data}

    await self.channel_layer.group_send(recipient_group_name, {
        'type': 'message_received',
        'content': content
    })

    await self.channel_layer.group_send(self.user_group_name, {
        'type': 'message_sent',
        'content': content
    })


async def handle_typing(self, content):
    try:
        recipient_id = content['recipient_id']
        isTyping = content['isTyping']
    except KeyError:
        await self.send(json.dumps({
            'type': 'critical_error', 
            'content': {'error': 'Datos incompletos'}
        }))
        return

    recipient_group_name = f'user_{recipient_id}'
    await self.channel_layer.group_send(recipient_group_name, {
        'type': 'typing',
        'content': {'id': recipient_id, 'isTyping': isTyping}
    })


async def handle_seen(self, content):
    try:
        recipient_id = content['recipient_id']
        chat_id = f'{min(int(self.user_id), int(recipient_id))}_{max(int(self.user_id), int(recipient_id))}'
    except KeyError:
        await self.send(json.dumps({
            'type': 'critical_error', 
            'content': {'error': 'Datos incompletos'}
        }))
        return

    await sync_to_async(change_seen)(chat_id)
