import factory
from Cats.models import Cat, Breed, CatRating

class BreedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Breed

class CatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cat

class CatRatingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CatRating
