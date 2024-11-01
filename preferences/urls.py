from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PreferencesViewSet, UserPreferencesViewSet, CheckUserPreferencesView, PreferenceMatchesView

router = DefaultRouter()
router.register(r'', PreferencesViewSet, basename='preferences')

urlpatterns = [
    path('user/', UserPreferencesViewSet.as_view(
        {'get': 'list', 'put': 'update'}), name='user-preferences'),
    path('user/<str:username>/', CheckUserPreferencesView.as_view(
        {'get': 'get_user_preferences'}), name='check-user-preferences'),
    path('matches/', PreferenceMatchesView.as_view({
        'get': 'find_matches'
    }), name='preference-matches'),
    path('', include(router.urls)),
]
