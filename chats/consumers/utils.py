
from datetime import datetime, timedelta
from pytz import timezone

def get_init_chats(user_id):
    from myApp.models import Chat, Messages, UserData
    user = UserData.objects.get(id=user_id)
    chats = Chat.objects.filter(chat_user1=user) | Chat.objects.filter(chat_user2=user)
    chat_data_list = []

    for chat in chats:
        chat_user = None
        if str(chat.chat_user1.id) == str(user_id):
            chat_user = UserData.objects.get(id=str(chat.chat_user2.id))
            seen = chat.chat_seen_user1
        elif str(chat.chat_user2.id) == str(user_id):
            chat_user = UserData.objects.get(id=str(chat.chat_user1.id))
            seen = chat.chat_seen_user2

        if not chat_user:
            continue

        last_message = Messages.objects.filter(messages_chat=chat).order_by('-messages_date').first()
        last_message_data = None
        if last_message:
            last_message_data = {
                'id': last_message.messages_id,
                'content': last_message.messages_content,
                'date': last_message.messages_date.isoformat()
            }

        chat_data = {
            'id': chat.chat_id,
            'date': chat.chat_date.isoformat(),
            'seenChat': seen,
            'user': {
                'id': chat_user.id,
                'name': chat_user.name,
                'email': chat_user.email,
                'userPhoto': chat_user.users_photo,
                'rol': chat_user.users_rol.rol_name,
            },
            'lastMessage': last_message_data
        }

        chat_data_list.append(chat_data)

    return chat_data_list


def get_init_messages(user_id):
    from myApp.models import Chat, Messages, UserData
    user = UserData.objects.only('id').get(id=user_id) 
    chats = Chat.objects.filter(chat_user1=user).values_list('chat_id', flat=False) | Chat.objects.filter(chat_user2=user).values_list('chat_id', flat=False) 
    messages_data_list = []
    for chat_id in chats:
        # Obtener los últimos 10 mensajes del chat
        messages = Messages.objects.filter(messages_chat=chat_id).order_by('-messages_date')

        for message in reversed(messages):  # Revertir para mantener el orden cronológico
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


def get_init_contacts(user_id, rol):
    from myApp.models import UserData, Chat

    # Diccionario que mapea el rol del usuario a los roles de contactos que puede obtener
    rol_contacts_map = {
        '1': [2, 3],  # Administrador puede ver coordinadores y donadores
        '2': [1, 4],  # Coordinador puede ver administradores y voluntarios
        '3': [1],     # Donador puede ver administradores
        '4': [2, 4, 5],  # Voluntario puede ver coordinadores, voluntarios, beneficiarios
        '5': [4]      # Beneficiario puede ver voluntarios
    }

    # Obtén el usuario
    user = UserData.objects.only('id').get(id=user_id)

    # Obtén los roles de contactos según el rol del usuario
    roles_to_fetch = rol_contacts_map.get(str(rol), [])

    # Si no hay roles para buscar, retorna una lista vacía
    if not roles_to_fetch:
        return []

    # Obtiene los contactos según los roles definidos
    contacts = UserData.objects.filter(users_rol__in=roles_to_fetch)

    # Excluye los usuarios con los que ya se tiene un chat abierto
    open_chats = Chat.objects.filter(chat_user1=user) | Chat.objects.filter(chat_user2=user)
    chat_user_ids = open_chats.values_list('chat_user1__id', 'chat_user2__id')
    exclude_user_ids = {uid for chat in chat_user_ids for uid in chat if uid != user.id}
    contacts = contacts.exclude(id__in=exclude_user_ids)

    # Generar los datos de los contactos con chat falso
    contacts_data = [
        {
            'id': f'{min(int(user_id), int(contact.id))}_{max(int(user_id), int(contact.id))}',
            'date': '',
            'seenChat': True,
            'user': {
                'id': contact.id,
                'name': contact.name,
                'email': contact.email,
                'userPhoto': contact.users_photo,
                'rol': contact.users_rol.rol_name
            },
            'lastMessage': None
        }
        for contact in contacts
    ]

    return contacts_data

def change_seen(chat_id):
    from myApp.models import Chat
    chat = Chat.objects.get(chat_id=chat_id)
    chat.chat_seen_user1 = True
    chat.chat_seen_user2 = True
    chat.save()


def get_chat(chat_id):
    from myApp.models import Chat
    try:
        return Chat.objects.get(chat_id=chat_id)
    except Chat.DoesNotExist:
        return None


def create_chat(chat_id, user1, user2):
    from myApp.models import Chat, UserData
    try:
        user1_instance = UserData.objects.get(id=user1)
        user2_instance = UserData.objects.get(id=user2)
        chat = Chat.objects.create(chat_id=chat_id, chat_date=datetime.now(timezone('America/Mexico_City')), chat_user1=user1_instance, chat_user2=user2_instance, chat_seen_user1=True, chat_seen_user2=False)
        return chat
    except UserData.DoesNotExist:
        return None


def create_message(message_id, message_content, date, user_id, chat_id):
    from myApp.models import Messages, UserData, Chat
    try:
        user = UserData.objects.get(id=user_id)
        chat = Chat.objects.get(chat_id=chat_id)
        date_obj = datetime.fromisoformat(date) + timedelta(hours=6)
        message = Messages.objects.create(messages_id=message_id, messages_content=message_content, messages_date=date_obj, messages_user=user, messages_chat=chat)
        return message
    except (UserData.DoesNotExist, Chat.DoesNotExist):
        return None


def serialize_chat(chat, recipient_id, message_id, message, date):
    user1 = chat.chat_user1
    user2 = chat.chat_user2
    user = user1 if user1.id != recipient_id else user2
    seen = chat.chat_seen_user1 if str(user1.id) == str(recipient_id) else chat.chat_seen_user2
    return {
            'id': chat.chat_id,
            'date': chat.chat_date.isoformat(),
            'seenChat': seen,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'userPhoto': user.users_photo,
                'rol': user.users_rol.rol_name
            },
            'lastMessage': {
                'id': message_id,
                'content': message,
                'date': date
            }
    }
