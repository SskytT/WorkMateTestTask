from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Breed(models.Model):
    name = models.CharField(max_length=100, verbose_name="название")

    class Meta:
        verbose_name = "Порода"
        verbose_name_plural = "Породы"

    def __str__(self):
        return self.name + " " + str(self.pk)


class Cat(models.Model):
    color = models.CharField(max_length=100, verbose_name="цвет")
    age = models.IntegerField(verbose_name="возраст")
    description = models.TextField(max_length=1000, verbose_name="описание")
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, verbose_name="порода")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="владелец")

    class Meta:
        verbose_name = "Кот"
        verbose_name_plural = "Коты"

    def __str__(self):
        return self.color + " " + str(self.breed) + " " + str(self.age) + " месяцев"


class Rating(models.IntegerChoices):
    ONE = 1, '1'
    TWO = 2, '2'
    THREE = 3, '3'
    FOUR = 4, '4'
    FIVE = 5, '5'


class CatRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="пользователь")
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, verbose_name="кот")
    value = models.IntegerField(choices=Rating.choices, validators=[MinValueValidator(Rating.ONE), MaxValueValidator(Rating.FIVE)])

    class Meta:
        verbose_name = "Оценка кота"
        verbose_name_plural = "Оценки котов"

    def __str__(self):
        return str(self.user.username) + " " + str(self.cat.pk) + " " + str(self.value)

