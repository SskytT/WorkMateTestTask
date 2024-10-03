import pytest
import factory
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from Cats.models import Cat, Breed, CatRating
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


class BreedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Breed


class CatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cat


class CatRatingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CatRating


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="testpassword")


@pytest.fixture
def auth_client(user):
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.fixture
def breed_factory():
    def create_breed(name):
        return BreedFactory.create(name=name)
    return create_breed


@pytest.fixture
def cat_factory():
    def create_cat(**kwargs):
        return CatFactory.create(**kwargs)
    return create_cat


@pytest.fixture
def cat_rating_factory():
    def create_cat_rating(**kwargs):
        return CatRatingFactory.create(**kwargs)
    return create_cat_rating


@pytest.fixture
def user_factory():
    def create_user(**kwargs):
        return UserFactory.create(**kwargs)
    return create_user


@pytest.mark.django_db
def test_register_user(client):
    url = reverse('register')
    data = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['message'] == 'User created successfully'
    assert User.objects.filter(username="testuser").exists()


@pytest.mark.django_db
def test_register_user_duplicate(client):
    url = reverse('register')
    data = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED

    response = client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['username'] == ['Пользователь с таким именем уже существует.']


@pytest.mark.django_db
def test_get_breed_list(auth_client, breed_factory):
    breed_factory(name='Persian')
    breed_factory(name='Siamese')

    url = reverse('breed')
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]['name'] == 'Persian'


@pytest.mark.django_db
def test_create_cat(auth_client, breed_factory):
    breed = breed_factory(name='Siamese')

    url = reverse('cat-list')
    data = {
        "color": "black",
        "age": 2,
        "description": "Friendly cat",
        "breed": breed.pk
    }
    response = auth_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['color'] == "black"
    assert response.data['breed'] == breed.pk


@pytest.mark.django_db
def test_get_cat_list(auth_client, cat_factory, breed_factory, user_factory):
    breed = breed_factory(name='Siamese')
    user = user_factory(username='testuser1', password='testpassword1')
    cat_factory(color='black', age=2, description='Friendly black cat', breed=breed, user=user)
    cat_factory(color='white', age=3, description='Cute white cat', breed=breed, user=user)

    url = reverse('cat-list')
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2



@pytest.mark.django_db
def test_filter_cats_by_breed(auth_client, cat_factory, breed_factory, user_factory):
    breed1 = breed_factory(name='Persian')
    breed2 = breed_factory(name='Siamese')
    user = user_factory(username='testuser1', password='testpassword1')
    cat_factory(color='black', age=2, description='Friendly black cat', breed=breed1, user=user)
    cat_factory(color='white', age=3, description='Cute white cat', breed=breed2, user=user)

    url = reverse('cat-list') + f'?breed={breed1.pk}'
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['breed'] == breed1.pk


@pytest.mark.django_db
def test_rate_cat(auth_client, cat_factory, user_factory, breed_factory):
    breed = breed_factory(name='Persian')
    user = user_factory(username='testuser1', password='testpassword1')
    cat = cat_factory(color='black', age=2, description='Friendly black cat', breed=breed, user=user)

    url = reverse('cat-rate-cat', kwargs={'pk': cat.pk})
    data = {"value": 5}
    response = auth_client.post(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == 'Rating saved or updated successfully.'


@pytest.mark.django_db
def test_get_cat_rating(auth_client, cat_factory, cat_rating_factory, user_factory, breed_factory):
    breed = breed_factory(name='Persian')
    user1 = user_factory(username='testuser1', password='testpassword1')
    user2 = user_factory(username='testuser2', password='testpassword2')
    cat = cat_factory(color='black', age=2, description='Friendly black cat', breed=breed, user=user1)
    cat_rating_factory(cat=cat, value=5, user=user1)
    cat_rating_factory(cat=cat, value=4, user=user2)

    url = reverse('cat-rating', kwargs={'pk': cat.pk})
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]['value'] == 5
    assert response.data[1]['value'] == 4


@pytest.mark.django_db
def test_cat_serializer_includes_rating_info(auth_client, cat_factory, cat_rating_factory, breed_factory, user_factory):
    breed = breed_factory(name='Persian')
    user1 = user_factory(username='testuser1', password='testpassword1')
    user2 = user_factory(username='testuser2', password='testpassword2')
    cat = cat_factory(color='black', age=2, description='Friendly black cat', breed=breed, user=user1)
    cat_rating_factory(cat=cat, value=5, user=user1)
    cat_rating_factory(cat=cat, value=4, user=user2)

    url = reverse('cat-detail', kwargs={'pk': cat.pk})
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['rating_count'] == 2
    assert response.data['rating_average'] == 4.5

@pytest.mark.django_db
def test_delete_stranger_cat(auth_client, cat_factory, breed_factory, user_factory):
    breed = breed_factory(name='Persian')
    user1 = user_factory(username='testuser1', password='testpassword1')
    cat = cat_factory(color='black', age=2, description='Friendly black cat', breed=breed, user=user1)

    url = reverse('cat-detail', kwargs={'pk': cat.pk})
    response = auth_client.delete(url)
    assert response.status_code == 403
    assert response.data['detail'] == 'У вас недостаточно прав для выполнения данного действия.'

@pytest.mark.django_db
def test_create_cat_without_authentication(client, breed_factory):
    breed = breed_factory(name='Siamese')
    url = reverse('cat-list')
    data = {
        "color": "black",
        "age": 2,
        "description": "Friendly cat",
        "breed": breed.pk
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data['detail'] == 'Учетные данные не были предоставлены.'

@pytest.mark.django_db
def test_rate_cat(auth_client, cat_factory, user_factory, breed_factory):
    breed = breed_factory(name='Persian')
    user = user_factory(username='testuser1', password='testpassword1')
    cat = cat_factory(color='black', age=2, description='Friendly black cat', breed=breed, user=user)

    url = reverse('cat-rate-cat', kwargs={'pk': cat.pk})
    data = {"value": 5}
    response = auth_client.post(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == 'Rating saved or updated successfully.'


@pytest.mark.django_db
def test_rate_cat_update(auth_client, cat_factory, breed_factory, cat_rating_factory, user_factory):
    breed = breed_factory(name='Persian')
    user = user_factory(username='testuser1', password='testpassword1')
    cat = cat_factory(color='black', age=2, description='Friendly black cat', breed=breed, user=user)
    url = reverse('cat-rate-cat', kwargs={'pk': cat.pk})

    data = {"value": 5}
    response = auth_client.post(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == 'Rating saved or updated successfully.'

    updated_data = {"value": 3}
    response = auth_client.post(url, updated_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == 'Rating saved or updated successfully.'

    url_rating = reverse('cat-rating', kwargs={'pk': cat.pk})
    rating_response = auth_client.get(url_rating)

    assert rating_response.status_code == status.HTTP_200_OK
    assert len(rating_response.data) == 1
    assert rating_response.data[0]['value'] == 3
