from django.urls import path

from .views import (
    LoginView, LogoutView, RegisterView,
    PricesView,
    ShopsView, ShopView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='api-login'),
    path('logout/', LogoutView.as_view(), name='api-logout'),
    path('register/', RegisterView.as_view(), name='api-register'),

    path('prices/', PricesView.as_view(), name='prices'),
    path('shops/', ShopsView.as_view(), name='shops'),
    path('shops/<pk>/', ShopView.as_view(), name='shop-item'),
]
