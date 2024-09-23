from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ChildrensViewSet


# Configuración del Router
router = DefaultRouter()
router.register(r'childrens', ChildrensViewSet, basename='childrens')


urlpatterns = router.urls
