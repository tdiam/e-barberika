from django.urls import path

from project.token_auth.views import ObtainTokenLoginView

urlpatterns = [
    path('login/', ObtainTokenLoginView.as_view(), name='api-login'),
]
