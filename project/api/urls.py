from django.urls import path

from project.api.views import PricesView
from project.token_auth.views import ObtainTokenLoginView

urlpatterns = [
    path('login/', ObtainTokenLoginView.as_view(), name='api-login'),

    path('prices/', PricesView.as_view(), name='prices')
]
