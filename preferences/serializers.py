from rest_framework import serializers
from .models import Preferences
from django.contrib.auth import get_user_model


class PreferencesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Preferences
        fields = ['id', 'name']


class UserMatchSerializer(serializers.ModelSerializer):
    """
    Serializer para mostrar usuarios con sus métricas de coincidencia
    """
    # Campos calculados en la consulta
    # Número de preferencias coincidentes
    matching_preferences_count = serializers.IntegerField()
    # Total de preferencias del usuario
    total_preferences = serializers.IntegerField()

    # Campos calculados en el serializer
    # Porcentaje de coincidencia
    matching_percentage = serializers.SerializerMethodField()
    # Lista de preferencias coincidentes
    matching_preferences = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'username',
            'matching_preferences_count',
            'total_preferences',
            'matching_percentage',
            'matching_preferences'
        ]

    def get_matching_percentage(self, obj):
        """
        Calcula el porcentaje de coincidencia entre dos usuarios.
        La fórmula considera tanto:
        - Qué porcentaje de mis preferencias coincide con el otro usuario
        - Qué porcentaje de sus preferencias coincide conmigo
        """
        # Obtener el número total de preferencias del usuario actual
        user_preferences_count = self.context['request'].user.preferences.count(
        )

        if user_preferences_count == 0 or obj.total_preferences == 0:
            return 0

        # Calcular porcentajes en ambas direcciones
        percentage_of_my_preferences = (
            obj.matching_preferences_count / user_preferences_count) * 100
        percentage_of_their_preferences = (
            obj.matching_preferences_count / obj.total_preferences) * 100

        # Calcular el promedio de ambos porcentajes
        average_percentage = (percentage_of_my_preferences +
                              percentage_of_their_preferences) / 2
        return round(average_percentage, 1)

    def get_matching_preferences(self, obj):
        """
        Obtiene la lista de preferencias que coinciden entre los usuarios
        """
        # Obtener preferencias del usuario actual
        user_preferences = self.context['request'].user.preferences.all()
        # Filtrar las preferencias del otro usuario que coinciden
        matching_preferences = obj.preferences.filter(id__in=user_preferences)

        return PreferencesSerializer(matching_preferences, many=True).data
