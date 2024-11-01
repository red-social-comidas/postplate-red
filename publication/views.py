from .models import Publication, Files
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .serializers import PublicationSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound


CustomUser = get_user_model()


class PublicationViewSet(viewsets.ModelViewSet):
    """Muestra todas las publicaciones en la pagina principal (home)"""
    # Usa el serializer "PublicationSerializer" para convertir las publicaciones a formato JSON.
    serializer_class = PublicationSerializer

    # Define qué publicaciones se van a mostrar, en este caso, todas las publicaciones en la base de datos.
    queryset = Publication.objects.all().order_by('-publication_date')

    # Permite que cualquier persona (sin necesidad de iniciar sesión) pueda ver las publicaciones.
    permission_classes = [AllowAny]
    pagination_class = None
    # Solo permite el método "GET", que es el que se usa para obtener/leer datos (no se puede crear ni modificar desde aquí).
    http_method_names = ['get']


class UserPublicationViewSet(viewsets.ModelViewSet):
    """Muestra las publicaciones del usuario que ha iniciado sesion (publicaciones de su propio perfil)"""
    # Usa el mismo serializer que antes, "PublicationSerializer".
    serializer_class = PublicationSerializer

    # Solo permite que los usuarios autenticados puedan ver sus propias publicaciones.
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        user = self.request.user
        # files = Files.objects.filter(publication=id)
        return Publication.objects.filter(id_user=user).order_by('-publication_date')

    def perform_create(self, serializer):
        files = self.request.FILES.getlist('files[]')
        serializer.save(id_user=self.request.user, files=files)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        message = {"mensaje": "Publication deleted successfully"}
        return Response(message, status=status.HTTP_200_OK)




# Muestra el perfil de un usuario
class ProfilePublicationViewSet(viewsets.ModelViewSet):
    """Muestra todas las publicaciones de un usuario"""
    # Usa el serializer "PublicationSerializer" para convertir las publicaciones a formato JSON.
    serializer_class = PublicationSerializer

    # Define qué publicaciones se van a mostrar, en este caso, todas las publicaciones en la base de datos.
    queryset = Publication.objects.all().order_by('-publication_date')

    # Pide sesión iniciada para mostrar el perfil
    permission_classes = [IsAuthenticated]


    # Solo permite el método "GET", que es el que se usa para obtener/leer datos (no se puede crear ni modificar desde aquí).
    http_method_names = ['get']
    
    @action(detail=False, methods=['get'], url_path='user/(?P<username>[^/.]+)')
    def by_username(self, request, username=None):
      try:
        user = CustomUser.objects.get(username=username)
      except CustomUser.DoesNotExist:
        raise NotFound('Usuario no encontrado')
      
      publications = Publication.objects.filter(id_user=user).order_by('-publication_date')
      serializer = self.get_serializer(publications, many=True)
      return Response(serializer.data)
      