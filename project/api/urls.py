from django.urls import path

from .views import (
    LoginView, LogoutView, RegisterView,
    PricesView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='api-login'),
    path('logout/', LogoutView.as_view(), name='api-logout'),
    path('register/', RegisterView.as_view(), name='api-register'),

    path('prices/', PricesView.as_view(), name='prices')
]
