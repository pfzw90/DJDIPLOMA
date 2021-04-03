import uuid

import pytest
from model_bakery import baker
from rest_framework.test import APIClient



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
def review_factory():
    def factory(**kwargs):
        return baker.make("ProductReview", **kwargs)

    return factory
