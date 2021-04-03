import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework import status


@pytest.mark.django_db
def test_products_create(api_client, product_factory):
    products = product_factory(_quantity=5)
    url = reverse("products-list")

    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    assert [product['id'] for product in resp.json()] == [product.id for product in products]
    assert len(resp.json()) == 5

@pytest.mark.django_db
def test_products_create_user(client):
    data = {"name" : "product1", "price" : 1000, "description" : "test"}
    url = reverse("products-list")

    resp = client.post(url, data=data)
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_products_create_admin(admin_client):
    data = {"name" : "product1", "price" : 1000, "description" : "test"}
    url = reverse("products-list")

    resp = admin_client.post(url, data=data)
    assert resp.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_products_filter_name(api_client, product_factory):
    products = product_factory(_quantity=5)
    url = reverse("products-list")

    for product in products:
        resp = api_client.get(url, {'name': product.name})
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()[0]['name'] == product.name
        assert len(resp.json()) == 1

@pytest.mark.django_db
def test_products_order_price(api_client,product_factory):
    product_factory(_quantity=5)
    url = reverse("products-list")

    resp = api_client.get(url, {'ordering': 'price'})
    resp_products = resp.json()
    print(resp_products)
    assert resp.status_code == status.HTTP_200_OK
    assert all(resp_products[i].get('price') <= resp_products[i + 1].get('price') for i in range(len(resp_products) - 1))
