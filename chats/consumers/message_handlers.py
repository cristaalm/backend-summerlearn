import uuid
import json
from datetime import datetime, timedelta
from asgiref.sync import sync_to_async
from .utils import get_init_chats, get_init_messages, change_seen, get_chat, create_chat, create_message, serialize_chat, get_init_contacts


# ? ######################### Funciones para la primera petición del front ######################### ? #

async def handle_start_chats(self):
    """
    <h3>Maneja la inicialización de los chats.</h3>

    <b>Atributos:</b>
    <ul>
        <li><b>self.user_id</b> (int): El ID del usuario.</li>
    </ul>

    <b>Retorna:</b>
    <ul>
        <li>Envía una respuesta JSON con los chats iniciales.</li>
    </ul>
    """
    user_id = self.user_id
    chats = await sync_to_async(get_init_chats)(user_id)
    await self.send(json.dumps({
        'type': 'init_chats',
        'content': chats
    }))

async def handle_init_messages(self):
    user_id = self.user_id

    messages = await sync_to_async(get_init_messages)(user_id)
    await self.send(json.dumps({
        'type': 'init_messages',
        'content': messages
    }))
    
async def handle_start_contacts(self):
    """
    <h3>Maneja la inicialización de los contactos.</h3>

    <b>Atributos:</b>
    <ul>
        <li><b>self.user_id</b> (int): El ID del usuario.</li>
        <li><b>self.user_rol</b> (int): El rol del usuario.</li>
    </ul>

    <b>Retorna:</b>
    <ul>
        <li>Envía una respuesta JSON con los contactos iniciales.</li>
    </ul>
    """
    user_id = self.user_id
    contacts = await sync_to_async(get_init_contacts)(user_id, self.user_rol)
    await self.send(json.dumps({
        'type': 'init_contacts',
        'content': contacts
    }))

# ? ######################### Funcion para el envío de mensajes ######################### ? #

async def handle_send_message(self, content):
    """
    <h3>Maneja el envío de un mensaje.</h3>

    <b>Atributos:</b>
    <ul>
        <li><b>self.user_id</b> (int): El ID del usuario que envía el mensaje.</li>
        <li>content (dict): El contenido del mensaje, incluyendo 'message', 'recipient_id' y 'date'.</li>
        <ul>
            <li><b>content.message</b> (str): El contenido del mensaje.</li>
            <li><b>content.recipient_id</b> (int): El ID del destinatario.</li>
            <li><b>content.date</b> (str): La fecha del mensaje en formato ISO.</li>
        </ul>
    </ul>

    <b>Retorna:</b>
    <ul>
        <li>Envía una respuesta JSON indicando el éxito o fracaso del envío del mensaje.</li>
    </ul>
    """
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

    date = datetime.fromisoformat(date) + timedelta(hours=6)
    # hacemos que el date sea serializable
    date = date.isoformat()

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

# ? ######################### Funcion para el estado de escritura ######################### ? #

async def handle_typing(self, content):
    """
    <h3>Maneja el estado de escritura.</h3>

    <b>Atributos:</b>
    <ul>
        <li>content (dict): El contenido del estado de escritura, incluyendo 'recipient_id' y 'isTyping'.</li>
        <ul>
            <li><b>content.recipient_id</b> (int): El ID del destinatario.</li>
            <li><b>content.isTyping</b> (bool): Indica si el usuario está escribiendo.</li>
        </ul>
    </ul>

    <b>Retorna:</b>
    <ul>
        <li>Envía una respuesta JSON indicando el estado de escritura.</li>
    </ul>
    """
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
    chat_id = f'{min(int(self.user_id), int(recipient_id))}_{max(int(self.user_id), int(recipient_id))}'
    await self.channel_layer.group_send(recipient_group_name, {
        'type': 'typing',
        'content': {'id': chat_id, 'isTyping': isTyping}
    })

# ? ######################### Funcion para el estado de visto ######################### ? #

async def handle_seen(self, content):
    """
    <h3>Maneja el estado de visto de un chat.</h3>

    <b>Atributos:</b>
    <ul>
        <li>content (dict): El contenido del estado de visto, incluyendo 'recipient_id'.</li>
        <ul>
            <li><b>content.recipient_id</b> (int): El ID del destinat
        </ul>
    </ul>

    <b>Retorna:</b>
    <ul>
        <li>Envía una respuesta JSON indicando el estado de visto.</li>
    </ul>
    """
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
