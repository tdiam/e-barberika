from django.urls import path

from project.token_auth.views import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='api-login'),
]
