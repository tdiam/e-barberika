from django.urls import path

from .views import (
    LoginView, LogoutView, RegisterView,
    ProductsView, ProductView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='api-login'),
    path('logout/', LogoutView.as_view(), name='api-logout'),
    path('register/', RegisterView.as_view(), name='api-register'),
    path('products/', ProductsView.as_view(), name='products'),
    path('products/<pk>/', ProductView.as_view(), name='product-item'),
]