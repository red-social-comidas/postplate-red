import cloudinary.uploader

from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import LoginEmailSerializer, UserEmailSerializer, ProfileSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound

CustomUser = get_user_model()


class RegisterEmailViewSet(viewsets.ModelViewSet):
    serializer_class = UserEmailSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        if CustomUser.objects.filter(email=request.data.get('email')).exists():
            return Response({'error': 'User already exists.'}, status=status.HTTP_409_CONFLICT)

        if CustomUser.objects.filter(username=request.data.get('username')).exists():
            return Response({'error': 'Username already exists.'}, status=status.HTTP_409_CONFLICT)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        message = {"message": "Register successfully"}
        return Response(message, status=status.HTTP_201_CREATED)


class LoginEmailViewSet(viewsets.ViewSet):
    serializer_class = LoginEmailSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        user.last_login = timezone.now()
        user.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class ProfileViewSet(viewsets.ViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'delete']
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return get_object_or_404(CustomUser, id=self.request.user.id)

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            serializer = self.serializer_class(
                user,
                data=request.data,
                partial=True,
                context={'request': request}
            )

            if serializer.is_valid():
                # La lógica de actualización de imagen está en el serializer
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {'error': f'Error al actualizar el perfil: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            if user.image_public_id:  # Usar image_public_id en lugar de parsear la URL
                cloudinary.uploader.destroy(user.image_public_id)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {'error': f'Error al eliminar el perfil: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
# Vista para ver el perfil de otras cuentas


class FriendProfileViewSet(viewsets.ViewSet):
    """Muestra el perfil de un amigo (otro usuario)."""
    serializer_class = ProfileSerializer
    # Solo usuarios autenticados pueden ver perfiles
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def retrieve(self, request, pk=None):
        """Obtiene el perfil de un amigo usando su ID."""
        # Busca el perfil del usuario con el ID proporcionado o lanza un error 404 si no existe.
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Vista para ver el perfil de otras cuentas autenticados
class UsernameProfileViewSet(viewsets.ViewSet):
    """Muestra el perfil de un amigo (otro usuario)."""
    serializer_class = ProfileSerializer
    # Solo usuarios autenticados pueden ver perfiles
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    @action(detail=False, methods=['get'], url_path='(?P<username>[^/.]+)')
    def by_username(self, request, username=None):
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise NotFound('Usuario no encontrado')

        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
