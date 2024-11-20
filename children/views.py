from django.db import IntegrityError
from django.core.files.storage import default_storage
from myApp.settings import MEDIA_ROOT
import os
import uuid
import datetime

############################################

from myApp.models import Children, PerformanceBeneficiaries, Programs, Activities, SubscriptionsChildren, PerformanceBeneficiaries
############################################

from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import ChildrensSerializer, PerformanceBeneficiariesSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.decorators import action
from programs_activities.serializers import ProgramsSerializer

class ChildrensViewSet(viewsets.ModelViewSet):
    queryset = Children.objects.all()
    serializer_class = ChildrensSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        # Obtener el ID del usuario de los parámetros de la URL
        user_id = self.request.user.id
        queryset = Children.objects.all()
        # Si el parámetro 'user_id' está presente, filtrar las donaciones
        if user_id is not None:
            queryset = queryset.filter(children_user__id=user_id)
        return queryset

    def create(self, request, *args, **kwargs):
        # Obtenemos la imagen del request
        children_photo = request.data.get('children_photo', None)

        if children_photo is None:
            return Response({"message": "Children photo is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Guardamos la imagen en un directorio único
        try:
            ext = children_photo.name.split('.')[-1]
            filename = f'{uuid.uuid4()}.{ext}'
            path = os.path.join('childrenImages', filename)
            default_storage.save(path, children_photo)
            request.data['children_photo'] = f'media/childrenImages/{filename}'
        except Exception as e:
            return Response({"message": f"Error saving image: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Serializamos y validamos los datos
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        child = Children.objects.get(children_id=serializer.data['children_id'])
        self.suscribedChildren(child)

        return Response({"message": "Children successfully created", "data": serializer.data}, status=status.HTTP_201_CREATED)
    
    def suscribedChildren(self, child):
        grade = child.children_grade
        if grade is None:
            return

        today = datetime.date.today()
        activities = Activities.objects.filter(
            activities_program__programs_grade=grade,
            activities_program__programs_start__gte=today
        )

        if not activities.exists():
            return

        # Validar duplicados
        existing_subscriptions = SubscriptionsChildren.objects.filter(
            subscriptions_children_child=child,
            subscriptions_children_activity__in=activities
        ).values_list('subscriptions_children_activity', flat=True)

        new_activities = [activity for activity in activities if activity.activities_id not in existing_subscriptions]

        subscriptions = [
            SubscriptionsChildren(
                subscriptions_children_child=child,
                subscriptions_children_activity=activity
            )
            for activity in new_activities
        ]
        SubscriptionsChildren.objects.bulk_create(subscriptions)

        # Crear las entradas de PerformanceBeneficiaries
        subscriptions_instances = SubscriptionsChildren.objects.filter(
            subscriptions_children_child=child
        )
        performances = [
            PerformanceBeneficiaries(
                performance_beneficiaries_value=None,
                performance_beneficiaries_subscription=sub
            )
            for sub in subscriptions_instances
        ]
        PerformanceBeneficiaries.objects.bulk_create(performances)


    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        children_photo = request.data.get('children_photo', None)

        # Crear un diccionario mutable a partir de request.data
        data = request.data.copy()

        # Si se proporciona una nueva foto, la actualizamos
        if children_photo:
            # Elimina la foto anterior si existe
            if instance.children_photo:
                old_photo_path = instance.children_photo.replace('media/', '')
                old_photo_path = os.path.join(MEDIA_ROOT, old_photo_path)
                if os.path.exists(old_photo_path):
                    os.remove(old_photo_path)
                    if os.path.exists(old_photo_path):
                        return Response({'error': 'Failed to update image'}, status=status.HTTP_400_BAD_REQUEST)

            # Genera un nuevo nombre de archivo para la foto
            ext = children_photo.name.split('.')[-1]
            filename = f'{uuid.uuid4()}.{ext}'
            # Guarda la nueva foto en el directorio
            path = os.path.join('childrenImages', filename)
            default_storage.save(path, children_photo)
            # Actualiza el campo con la nueva ruta de la foto
            data['children_photo'] = f'media/childrenImages/{filename}'
        else:
            # Mantén la foto anterior si no se envía una nueva
            data['children_photo'] = instance.children_photo

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            "message": "Children successfully updated",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Elimina la foto de perfil si existe
        if instance.children_photo:
            # Construir la ruta completa del archivo a partir de la ruta almacenada
            photo_path = os.path.join(MEDIA_ROOT, instance.children_photo.replace('media/', ''))

            # Elimina el archivo si existe
            if os.path.exists(photo_path):
                os.remove(photo_path)
                if os.path.exists(photo_path):
                    return Response({'error': 'Failed to delete old image'}, status=HTTP_400_BAD_REQUEST)

        # Realiza la eliminación del objeto
        self.perform_destroy(instance)

        return Response({
            "message": "Children successfully deleted"
        }, status=status.HTTP_204_NO_CONTENT)




class PerformanceBeneficiariesViewSet(viewsets.ModelViewSet):
    queryset = PerformanceBeneficiaries.objects.all()
    serializer_class = PerformanceBeneficiariesSerializer
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    @action(detail=False, methods=['post'], url_path='save-scores')
    def save_scores(self, request):
        scores = request.data.get('scores', [])
        
        for score_data in scores:
            performance_id = score_data.get('id')
            grade = score_data.get('grade')
            
            try:
                # Cambiar 'id' por 'performance_beneficiaries_id'
                performance = PerformanceBeneficiaries.objects.get(performance_beneficiaries_id=performance_id)
                performance.performance_beneficiaries_value = grade  # Asegúrate de que 'performance_beneficiaries_value' es el campo correcto
                performance.save()
            except PerformanceBeneficiaries.DoesNotExist:
                return Response(
                    {"error": f"Performance with ID {performance_id} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response({"message": "Scores saved successfully"}, status=status.HTTP_200_OK)
    
