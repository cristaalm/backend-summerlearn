from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import SubscriptionsChildrenSerializer,SubscriptionsVolunteerSerializer

# Configuración del Router
router = DefaultRouter()
router.register(r'subscription-children', SubscriptionsChildrenSerializer, basename='subscription-children')
router.register(r'subscription-volunteer', SubscriptionsVolunteerSerializer, basename='subscription-volunteer')

urlpatterns = router.urls