from django.urls import path, include
from rest_framework import routers

from accounts.viewsets.userviewset import UserViewSet
# from accounts.viewsets.placeviewset import PlaceViewSet, PlaceReviewViewset

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
# router.register(r'places', PlaceViewSet, basename='place')
# router.register(r'reviews', PlaceReviewViewset, basename='review')

urlpatterns = [
    path('v1/', include(router.urls)),
]