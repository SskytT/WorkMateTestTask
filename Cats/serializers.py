from rest_framework import serializers
from .models import Cat, Breed, CatRating
from rest_framework.reverse import reverse
from django.db.models import Avg


class CatSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    rating_list_url = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    rating_average = serializers.SerializerMethodField()

    class Meta:
        model = Cat
        fields = ['pk', 'color', 'age', 'description', 'breed', 'user', 'rating_list_url', 'rating_count', 'rating_average']

    def get_rating_list_url(self, obj):
        request = self.context.get('request')
        return reverse('cat-rating', kwargs={'pk': obj.pk}, request=request)

    def get_rating_count(self, obj):
        return CatRating.objects.filter(cat=obj.pk).count()

    def get_rating_average(self, obj):
        return CatRating.objects.filter(cat=obj.pk).aggregate(Avg('value'))['value__avg']


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ['pk', 'name']


class CatRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatRating
        fields = ['cat', 'value', 'user']
