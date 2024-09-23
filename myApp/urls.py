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
    
    path('', include('programs_activities.urls')),
    path('', include('schedules.urls')),
    path('', include('donations.urls')),
    path('', include('children.urls')),
    path('', include(router.urls)),  # Incluye las URLs del router
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)