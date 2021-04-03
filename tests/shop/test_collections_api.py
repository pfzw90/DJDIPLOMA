import pytest
from django.urls import reverse
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
def test_collections_create_try_user(client):
    data = {"heading" : "collection1", "text" : "test", "products" : []}
    url = reverse("collections-list")

    resp = client.post(url, data=data)
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED

