from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from myApp.models import SubscriptionsChildren,SubscriptionsVolunteer
from .serializers import SubscriptionsChildrenSerializer,SubscriptionsVolunteerSerializer

class SubscriptionsChildrenSerializer(viewsets.ModelViewSet):
    queryset = SubscriptionsChildren.objects.all()
    serializer_class = SubscriptionsChildrenSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response({
            "message": "Child successfully created",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
        
class SubscriptionsVolunteerSerializer(viewsets.ModelViewSet):
    queryset = SubscriptionsVolunteer.objects.all()
    serializer_class = SubscriptionsVolunteerSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        id_user = request.data.get('subscriptions_volunteer_user', None)

        # Verificar si se proporcionó el ID del usuario
        if not id_user:
            return Response({'error': 'El campo subscriptions_volunteer_user es obligatorio.'}, status=status.HTTP_400_BAD_REQUEST)

        # Contar las suscripciones activas del usuario actual
        active_subscriptions = SubscriptionsVolunteer.objects.filter(
            subscriptions_volunteer_user=id_user
        ).count()

        # Verificar si el usuario ya tiene más de tres suscripciones
        if active_subscriptions >= 3:
            return Response({
                "error": "No puedes suscribirte a más actividades, ya tienes tres suscripciones activas."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Validar los datos
        serializer.is_valid(raise_exception=True)

        # Crear la nueva suscripción
        self.perform_create(serializer)

        return Response({
            "message": "Volunteer successfully created",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)