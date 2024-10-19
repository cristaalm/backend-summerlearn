# path: chats/controllers/serializers.py

from myApp.models import Chat, Messages, UserData
from rest_framework import serializers

# Serializer para la información del usuario
class UserSerializer(serializers.ModelSerializer):
    rol_name = serializers.CharField(source='users_rol.rol_name', read_only=True)

    class Meta:
        model = UserData
        fields = ['id', 'name', 'email', 'users_photo', 'rol_name']

class UserSerializerMessage(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['id', 'users_photo']

# Serializer para los chats
class ChatSerializer(serializers.ModelSerializer):
    chat_user = serializers.SerializerMethodField()  # Solo se devolverá un usuario
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['chat_id', 'chat_date', 'chat_user', 'last_message']

    def get_chat_user(self, obj):
        request = self.context.get('request', None)
        if request:
            user_id = request.query_params.get('user', None)
            # Verifica qué usuario no es el que está en los query_params
            if str(obj.chat_user1.id) == user_id:
                return UserSerializer(obj.chat_user2).data
            return UserSerializer(obj.chat_user1).data

    def get_last_message(self, obj):
        last_message = Messages.objects.filter(messages_chat=obj).order_by('-messages_date').first()
        if last_message:
            return {
                'id': last_message.messages_id,
                'content': last_message.messages_content,
                'date': last_message.messages_date
            }
        return None


class MessageSerializer(serializers.ModelSerializer):
    messages_user = UserSerializerMessage(read_only=True)

    class Meta:
        model = Messages
        fields = '__all__'
