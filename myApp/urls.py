from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CustomAPIRootView, UserViewSet, StatusViewSet, RolViewSet, RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .authenticate import Authenticate
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

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
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Custom API Root: Para poder cargar la vista personalizada del API Root en la URL raíz del proyecto (http://localhost:8000/)
    path('', CustomAPIRootView.as_view(), name='api-root'),

    # Incluir las URLs de otras apps: Seguir añadiendo las URLs de las otras apps
    path('', include('programs_activities.urls')),
    path('', include('schedules.urls')),
    path('', include('donations.urls')),
    path('', include('children.urls')),

    # Incluir las URLs del router al final
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)