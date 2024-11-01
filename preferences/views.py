from django.shortcuts import render
from rest_framework import viewsets, status
from .serializers import PreferencesSerializer, UserMatchSerializer
from .models import Preferences
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from django.db.models import Count, Q

CustomUser = get_user_model()


class PreferencesViewSet(viewsets.ModelViewSet):
    serializer_class = PreferencesSerializer
    queryset = Preferences.objects.all().order_by('id')
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]


class UserPreferencesViewSet(viewsets.GenericViewSet):
    serializer_class = PreferencesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Preferences.objects.filter(user_id=self.request.user).order_by('id')

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        preferences_ids = request.data.get("preferences", [])
        user = request.user

        # Clear existing preferences
        user.preferences.clear()

        # Add new preferences
        for pref_id in preferences_ids:
            try:
                preference = Preferences.objects.get(id=pref_id)
                user.preferences.add(preference)
            except Preferences.DoesNotExist:
                return Response(
                    {"error": f"Preferencia con ID {pref_id} no encontrada"},
                    status=status.HTTP_404_NOT_FOUND
                )

        return Response(
            {"message": "Preferencias actualizadas exitosamente"},
            status=status.HTTP_200_OK
        )


class CheckUserPreferencesView(viewsets.GenericViewSet):
    serializer_class = PreferencesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Preferences.objects.all().order_by('id')

    @action(detail=False, methods=['get'], url_path=r'(?P<username>[^/.]+)')
    def get_user_preferences(self, request, username=None):
        try:
            user = CustomUser.objects.get(username=username)
            preferences = Preferences.objects.filter(
                user_id=user
            ).select_related().order_by('id')

            serializer = self.get_serializer(preferences, many=True)
            return Response({
                'username': user.username,
                'preferences': serializer.data
            })

        except CustomUser.DoesNotExist:
            raise NotFound('Usuario no encontrado')


class PreferenceMatchesView(viewsets.GenericViewSet):
    """
    Vista para encontrar usuarios con preferencias similares.
    Hereda de GenericViewSet ya que solo necesitamos implementar 
    funcionalidad personalizada.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserMatchSerializer  # Crearemos este serializer

    def get_queryset(self):
        """
        Excluye al usuario actual del queryset base
        """
        return get_user_model().objects.exclude(id=self.request.user.id)

    @action(detail=False, methods=['get'])
    def find_matches(self, request):
        # Obtener las preferencias del usuario actual
        user_preferences = request.user.preferences.all()

        # Encontrar usuarios con preferencias similares
        similar_users = (
            get_user_model().objects
            .exclude(id=request.user.id)  # Excluir al usuario actual
            # Filtrar usuarios con preferencias similares
            .filter(preferences__in=user_preferences)
            # Añadir anotaciones (campos calculados) a cada usuario
            .annotate(
                matching_preferences_count=Count(
                    'preferences', filter=Q(preferences__in=user_preferences)),
                total_preferences=Count('preferences')
            )
            # Solo usuarios con al menos una preferencia en común
            .filter(matching_preferences_count__gt=0)
            # Ordenar por cantidad de coincidencias
            .order_by('-matching_preferences_count')
        )

        serializer = self.get_serializer(similar_users, many=True)
        return Response(serializer.data)
