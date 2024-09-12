from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from myApp.models import Areas, Programs
from .serializers import AreasSerializer, ProgramsSerializer

# Create your views here.

class AreasViewSet(viewsets.ModelViewSet):
    queryset = Areas.objects.all()
    serializer_class = AreasSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        data = request.data

        user_id = request.user.id
        data['areas_user'] = user_id  

        serializer = self.get_serializer(data=data)

        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response({
            "message": "Area successfully created",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

class ProgramsViewSet(viewsets.ModelViewSet):
    queryset = Programs.objects.all()
    serializer_class = ProgramsSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data

        user_id = request.user.id
        data['programs_user'] = user_id  

        serializer = self.get_serializer(data=data)

        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response({
            "message": "Program successfully created",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)