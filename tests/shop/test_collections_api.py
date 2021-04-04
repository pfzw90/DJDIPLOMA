import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework import status


@pytest.mark.django_db
def test_collections_get(api_client, collection_factory):
    collections = collection_factory(_quantity=5)
    url = reverse("collections-list")

    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    assert [collection['heading'] for collection in resp.json()] == [collection.heading for collection in collections]
    assert len(resp.json()) == 5


@pytest.mark.django_db
def test_collections_create_try_user(auth_user):
    data = {}
    url = reverse("collections-list")

    resp = auth_user.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_collections_create_try_admin(auth_admin):
    data = {"heading": "test", "text": "test", "products": [baker.make('Product').id]}
    url = reverse("collections-list")

    resp = auth_admin.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_201_CREATED
