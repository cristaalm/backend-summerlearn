# path: chats/views.py

from rest_framework import viewsets
from myApp.models import Chat, Messages, UserData
from .controllers.serializers import ChatSerializer, MessageSerializer

########################################################################################
# Importaciones de Django REST Framework
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny  
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from rest_framework.reverse import reverse 
from rest_framework_simplejwt.views import TokenObtainPairView
########################################################################################

# Vista para el CRUD de Chats
class ChatsViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user_id = self.request.query_params.get('user', None)
        if user_id is not None:
            try:
                user = UserData.objects.get(id=user_id)
            except UserData.DoesNotExist:
                return Response({'detail': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
            
            return Chat.objects.filter(chat_user1=user) | Chat.objects.filter(chat_user2=user)
        return Chat.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if isinstance(queryset, Response):
            return queryset
        if not queryset.exists():
            return Response([], status=status.HTTP_200_OK)

        # Pasar el contexto de la request al serializer
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

# Vista para el CRUD de Mensajes
class MessagesViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        chat_id = self.request.query_params.get('chat', None)
        if chat_id is not None:
            # Verifica si el chat existe
            try:
                chat = Chat.objects.get(chat_id=chat_id)
            except Chat.DoesNotExist:
                # Si el chat no existe, devuelve un error
                return Response({'detail': 'Chat no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
            
            # Filtra los mensajes por chat
            return Messages.objects.filter(messages_chat=chat)
        # Si no se especifica el chat, retorna un queryset vacío
        return Messages.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if isinstance(queryset, Response):
            # Si get_queryset devolvió un Response (error), lo retornamos directamente
            return queryset
        # Si no hay mensajes, devolvemos un array vacío
        if not queryset.exists():
            return Response([], status=status.HTTP_200_OK)
        return super().list(request, *args, **kwargs)