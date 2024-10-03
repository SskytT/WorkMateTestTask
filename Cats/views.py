from rest_framework import viewsets, generics, status
from .models import Cat, Breed, CatRating
from .serializers import CatSerializer, BreedSerializer, CatRatingSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError


class CatViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['breed', 'user']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], url_path='rate')
    def rate_cat(self, request, pk=None):
        cat = get_object_or_404(Cat, pk=pk)
        user = request.user
        value = request.data.get('value')
        for validator in CatRating._meta.get_field('value').validators:
            try:
                validator(int(value))
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        rating, created = CatRating.objects.update_or_create(
            user=user, cat=cat, defaults={'value': value}
        )

        return Response({'message': 'Rating saved or updated successfully.'})

    @action(detail=True, methods=['get'], url_path='rating')
    def rating(self, request, pk=None):
        cat = get_object_or_404(Cat, pk=pk)
        rating_list = CatRating.objects.filter(cat=cat)
        serializer = CatRatingSerializer(rating_list, many=True)
        return Response(serializer.data)


class BreedListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
