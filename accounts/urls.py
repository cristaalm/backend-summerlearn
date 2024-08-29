from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import status_list, rol_list
from accounts import views
from .authenticate import Authenticate  # Asegúrate de que Authenticate esté correctamente importado

# Configuración del Router
router = DefaultRouter()
router.register(r'users', Authenticate, basename='users')

urlpatterns = [
    # Incluir las URLs del Router
    path('', include(router.urls)),

    # Rutas personalizadas
    path('status/', status_list, name='status-list'),
    path('rol/', rol_list, name='rol-list'),
]
