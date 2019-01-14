from django.urls import path

from project.token_auth.views import ObtainTokenLoginView
from .views import (
    ProductsView, ProductView
)

urlpatterns = [
    path('login/', ObtainTokenLoginView.as_view(), name='api-login'),
    path('products/', ProductsView.as_view(), name='products'),
    path('products/<pk>/', ProductView.as_view(), name='product-item'),
]
