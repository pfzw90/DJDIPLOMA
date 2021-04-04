from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from shop.models import Order


def test_orders_get_unauthorized(api_client):
    url = reverse("orders-list")

    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_orders_create_unauthorized(api_client):
    data = {}
    url = reverse("orders-list")

    resp = api_client.post(url, data=data)
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_orders_create(auth_user):
    products = {'product': baker.make('Product').id, 'quantity': 1}
    data = {'order_products': [products]}
    url = reverse("orders-list")

    resp = auth_user.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_201_CREATED


def test_orders_change_status_user(auth_user):
    products = {'product': baker.make('Product').id, 'quantity': 1}
    data = {'order_products': [products]}
    url = reverse("orders-list")

    auth_user.post(url, data=data, format='json')

    data = {'status': 'IN PROGRESS'}
    url = reverse("orders-detail", args=(Order.objects.get().id,))

    resp = auth_user.patch(url, data=data, format='json')
    print(resp.json())

    assert resp.json().get("non_field_errors")[0] == "Менять статус заказа могут только администраторы"


def test_orders_get_user(auth_user, order_factory):
    order_factory(_quantity=5)

    products = {'product': baker.make('Product').id, 'quantity': 1}
    data = {'order_products': [products]}
    url = reverse("orders-list")

    post_resp_id = auth_user.post(url, data=data, format='json').json()['id']
    resp = auth_user.get(url).json()
    assert len(resp) == 1
    assert resp[0]['id'] == post_resp_id


def test_orders_get_admin(auth_admin, order_factory):
    order_factory(_quantity=5)
    url = reverse("orders-list")
    resp = auth_admin.get(url)
    assert len(resp.json()) == 5
