import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework import status


@pytest.mark.django_db
def test_reviews_get(api_client, review_factory):
    reviews = review_factory(_quantity=5)
    url = reverse("reviews-list")

    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    assert [review['product_id'] for review in resp.json()] == [review.product_id.id for review in reviews]
    assert len(resp.json()) == 5


def test_reviews_create_unauthorized(api_client):
    data = {"product_id": 1, "stars": 1, "text": "test"}
    url = reverse("reviews-list")

    resp = api_client.post(url, data=data)
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_reviews_create_double(auth_user):
    product = baker.make('Product')
    data = {"product_id": product.id, "stars": 1, "text": "test"}
    url = reverse("reviews-list")

    resp = auth_user.post(url, data=data)
    assert resp.status_code == status.HTTP_201_CREATED

    resp = auth_user.post(url, data=data)
    assert resp.json().get("non_field_errors")[0] == "У Вас уже есть отзыв по данному товару"
