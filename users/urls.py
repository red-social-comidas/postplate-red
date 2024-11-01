from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterEmailViewSet, LoginEmailViewSet, ProfileViewSet, FriendProfileViewSet, UsernameProfileViewSet

router = DefaultRouter()
router.register(r'register', RegisterEmailViewSet, basename='register')
router.register(r'login', LoginEmailViewSet, basename='login')
router.register(r'', FriendProfileViewSet, basename='by-id')
router.register(r'by-username', UsernameProfileViewSet, basename='by-username')

urlpatterns = [
    path('profile/', ProfileViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='profile'),
    path('', include(router.urls))
]
