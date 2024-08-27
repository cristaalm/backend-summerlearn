from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RolViewSet, StatusViewSet, UserViewSet

# Importa el enrutador predeterminado de Django REST Framework
router = DefaultRouter()

# Registra el ViewSet de 'User' en el enrutador
router.register(r'users', UserViewSet)
router.register(r'status', StatusViewSet)
router.register(r'rol', RolViewSet)
# Define la lista de rutas del enrutador
urlpatterns = router.urls