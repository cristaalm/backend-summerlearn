from rest_framework.routers import DefaultRouter
from .views import ChatsViewSet, MessagesViewSet
from django.urls import path, include

router = DefaultRouter()

router.register(r'chats', ChatsViewSet, basename='chats')
router.register(r'messages', MessagesViewSet, basename='messages')

urlpatterns = router.urls
