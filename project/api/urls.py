from django.urls import path

from .views import (
    LoginView, LogoutView, RegisterView,
    ProductsView, ProductView
    PricesView,
    ShopsView, ShopView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='api-login'),
    path('logout/', LogoutView.as_view(), name='api-logout'),
    path('register/', RegisterView.as_view(), name='api-register'),
  
    path('products/', ProductsView.as_view(), name='products'),
    path('products/<pk>/', ProductView.as_view(), name='product-item'),

    path('prices/', PricesView.as_view(), name='prices'),
  
    path('shops/', ShopsView.as_view(), name='shops'),
    path('shops/<pk>/', ShopView.as_view(), name='shop-item'),
]
