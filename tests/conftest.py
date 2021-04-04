import pytest
from model_bakery import baker
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture
def auth_user(api_client, django_user_model):
    user = django_user_model.objects.create_user(username="test", password="test")
    token = Token.objects.create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return api_client


@pytest.fixture
def auth_admin(api_client, django_user_model):
    user = django_user_model.objects.create_user(username="test", password="test", is_staff=True)
    token = Token.objects.create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return api_client


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def product_factory():
    def factory(**kwargs):
        return baker.make("Product", **kwargs)

    return factory


@pytest.fixture
def collection_factory():
    def factory(**kwargs):
        return baker.make("Collection", **kwargs)

    return factory


@pytest.fixture
def order_factory():
    def factory(**kwargs):
        return baker.make("Order", **kwargs)

    return factory


@pytest.fixture
def review_factory():
    def factory(**kwargs):
        return baker.make("ProductReview", **kwargs)

    return factory
