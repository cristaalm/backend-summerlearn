from django.db import IntegrityError
from django.core.files.storage import default_storage
import os
import uuid

############################################

from myApp.models import Children
############################################

from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import ChildrensSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

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