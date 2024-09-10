from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, StatusViewSet, RolViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .authenticate import Authenticate
from .views import RegisterView

# Configuración del Router
router = DefaultRouter()
router.register(r'auth', Authenticate, basename='authenticate')  # Cambié 'users' a 'auth'
# router.register(r'users', UserViewSet, basename='users')
router.register(r'rol', RolViewSet, basename='rol')
router.register(r'status', StatusViewSet, basename='status')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),  # Incluye las URLs del router
]
