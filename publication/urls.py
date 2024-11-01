from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PublicationViewSet, UserPublicationViewSet, ProfilePublicationViewSet

router = DefaultRouter()
router.register(r'feed', PublicationViewSet,
                basename='feed')
router.register(r'user-publications', UserPublicationViewSet,
                basename='user-publication')
router.register(r'by-username', ProfilePublicationViewSet,
                basename='by-username')

urlpatterns = [
    path('', include(router.urls)),
]
