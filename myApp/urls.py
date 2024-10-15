from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CustomAPIRootView, UserViewSet, StatusViewSet, RolViewSet, RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .authenticate import Authenticate
from .views import MyTokenObtainPairView
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import DecryptView
from .mails.send_mail import send_email_view
from .mails.keys import get_id_user, update_password_by_key

########################################################################################
# Configuración del Router
router = DefaultRouter()
router.register(r'auth', Authenticate, basename='authenticate')
router.register(r'users', UserViewSet, basename='users')
router.register(r'rol', RolViewSet, basename='rol')
router.register(r'status', StatusViewSet, basename='status')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/decrypt/', DecryptView.as_view(), name='decrypt'),

    # Custom API Root: Para poder cargar la vista personalizada del API Root en la URL raíz del proyecto (http://localhost:8000/)
    path('', CustomAPIRootView.as_view(), name='api-root'),

    # Incluir las URLs de otras apps: Seguir añadiendo las URLs de las otras apps
    path('', include('programs_activities.urls')),
    path('', include('schedules.urls')),
    path('', include('donations.urls')),
    path('', include('children.urls')),
    path('', include('subscriptions.urls')),
    path('', include('performance_beneficiaries.urls')),
    path('', include('chats.urls')),
    path('send_mail/', send_email_view, name='send_mail'),  # Ruta para enviar correo
    path('get_user/', get_id_user, name='get_user'),  # Ruta para generar key
    path('update_password/<str:key>/', update_password_by_key, name='change_password'),  # Ruta para cambiar contraseña

    # Incluir las URLs del router al final
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)