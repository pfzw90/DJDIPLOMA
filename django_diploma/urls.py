"""django_diploma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from shop.views import OrderViewSet, ProductViewSet, CollectionViewSet, ReviewViewSet

router = DefaultRouter()

router.register(r'orders', OrderViewSet, basename='api')
router.register(r'products', ProductViewSet, basename='api')
router.register(r'collections', CollectionViewSet, basename='api')
router.register(r'reviews', ReviewViewSet, basename='api')

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]

