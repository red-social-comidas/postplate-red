from rest_framework import serializers
from .models import Friends
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = ['id', 'id_user1', 'id_user2', 'state',
                  'application_date', 'acceptance_date']


class FriendListSerializer(serializers.ModelSerializer):
    friend = serializers.SerializerMethodField()

    class Meta:
        model = Friends
        fields = ['id', 'friend', 'state', 'application_date',
                  'acceptance_date', 'rejection_date']

    def get_friend(self, obj):
        request_user = self.context['request'].user
        if obj.id_user1 == request_user:
            return obj.id_user2.username
        return obj.id_user1.username
