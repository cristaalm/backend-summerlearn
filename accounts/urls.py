from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, StatusViewSet, RolViewSet
from accounts import views
from .authenticate import Authenticate  # Asegúrate de que Authenticate esté correctamente importado

# Configuración del Router
router = DefaultRouter()
router.register(r'users', Authenticate, basename='autehnticate')
router.register(r'users', UserViewSet, basename='users')
router.register(r'rol', StatusViewSet, basename='status')
router.register(r'status', RolViewSet, basename='rol')


urlpatterns = router.urls
