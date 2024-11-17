from django.db import IntegrityError
from django.core.files.storage import default_storage
from myApp.settings import STATIC_ROOT
import os
import uuid

############################################

from myApp.models import Children, PerformanceBeneficiaries
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

class ChildrensViewSet(viewsets.ModelViewSet):
    queryset = Children.objects.all()
    serializer_class = ChildrensSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):

        # obtenemos la imagen del request
        children_photo = request.data.get('children_photo', None)

        if children_photo is None:
            return Response({
                "message": "Children photo is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        # extraemos la extensión de la imagen
        ext = children_photo.name.split('.')[-1]
        # Creamos un nombre de archivo único
        filename = f'{uuid.uuid4()}.{ext}'
        # Juntamos el path con el nombre del archivo
        path = os.path.join('childrenImages', filename)
        # Guardamos la imagen en el directorio
        default_storage.save(path, children_photo)
        # Reemplazamos el campo children_photo con la ruta de la imagen
        request.data['children_photo'] = f'media/childrenImages/{filename}'

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response({
            "message": "Children successfully created",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    
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
                old_photo_path = os.path.join(STATIC_ROOT, old_photo_path)
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
            photo_path = os.path.join(STATIC_ROOT, instance.children_photo.replace('media/', ''))

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
    
