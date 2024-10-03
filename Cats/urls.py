from django.urls import path
from .views import CatViewSet, BreedListAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'cat', CatViewSet, basename='cat')


urlpatterns = [
    path('breed', BreedListAPIView.as_view(), name='breed')
]

urlpatterns += router.urls
