# Importa tus serializadores
from .serializers import FriendListSerializer, FriendRequestSerializer
from .models import Friends  # Asegúrate de importar tu modelo Friends
from .models import Friends
from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .serializers import FriendRequestSerializer, FriendListSerializer

CustomUser = get_user_model()


class FriendViewSet(viewsets.ModelViewSet):
    # Consulta para obtener todas las solicitudes de amistad, ordenadas por fecha de solicitud (más recientes primero)
    queryset = Friends.objects.all().order_by('-application_date')
    # Permite solo a usuarios autenticados acceder a esta vista
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        return Friends.objects.filter(
            Q(id_user1=user) | Q(id_user2=user)
        ).order_by('-application_date')

    def get_serializer_class(self):
        """
        Devuelve el serializador adecuado según la acción que se esté realizando.
        - 'list' o 'friends': utiliza FriendListSerializer
        - Para otras acciones: utiliza FriendRequestSerializer
        """
        if self.action == 'list' or self.action == 'friends':
            return FriendListSerializer
        return FriendRequestSerializer

    # Crear solicitud de amistad
    def create(self, request, *args, **kwargs):
        # Obtiene el ID del usuario al que se desea enviar la solicitud de amistad
        id_user2 = request.data.get('id_user2')
        # Verifica que se haya proporcionado el ID
        if not id_user2:
            return Response({'detail': 'Debes proporcionar el ID del usuario al que deseas enviar la solicitud.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Verifica si ya existe una solicitud de amistad entre los usuarios
        if Friends.objects.filter(id_user1=request.user, id_user2_id=id_user2).exists():
            return Response({'detail': 'Ya has enviado una solicitud a este usuario.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Crea la solicitud de amistad
        friend_request = Friends.objects.create(
            id_user1=request.user, id_user2_id=id_user2)
        serializer = self.get_serializer(friend_request)
        # Retorna la solicitud de amistad creada con un estado HTTP 201
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Aceptar solicitud de amistad
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        # Obtiene la solicitud de amistad correspondiente al ID en la URL
        friend_request = self.get_object()
        # Verifica que el usuario autenticado sea quien puede aceptar la solicitud
        if friend_request.id_user2 != request.user:
            return Response({'detail': 'No puedes aceptar esta solicitud.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Cambia el estado de la solicitud a aceptada
        friend_request.accept()
        return Response({'detail': 'Solicitud de amistad aceptada.'})

    # Rechazar solicitud de amistad
    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        # Obtiene la solicitud de amistad correspondiente al ID en la URL
        friend_request = self.get_object()
        # Verifica que el usuario autenticado sea quien puede rechazar la solicitud
        if friend_request.id_user2 != request.user:
            return Response({'detail': 'No puedes rechazar esta solicitud.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Cambia el estado de la solicitud a rechazada
        friend_request.decline()
        return Response({'detail': 'Solicitud de amistad rechazada.'})

    # Listar amigos
    @action(detail=False, methods=['get'])
    def list_friends(self, request):
        user = request.user
        # Filtra los amigos aceptados, tanto si el usuario es el que envió la solicitud (id_user1)
        # como si fue el que la recibió (id_user2)
        friends = Friends.objects.filter(
            (Q(id_user1=user) | Q(id_user2=user)), state='accepted').order_by('-acceptance_date')
        # Serializa los amigos encontrados
        serializer = self.get_serializer(
            friends, many=True, context={'request': request})
        return Response(serializer.data)

    # Ver las solicitudes pendientes enviadas y recibidas
    @action(detail=False, methods=['get'])
    def pending(self, request):
        user = request.user
        # Filtra las solicitudes pendientes enviadas por el usuario o recibidas por él
        requests = Friends.objects.filter(
            Q(id_user1=user, state='pending') | Q(id_user2=user, state='pending')).order_by('-application_date')
        # Serializa las solicitudes pendientes
        serializer = self.get_serializer(requests, many=True)
        return Response(serializer.data)
