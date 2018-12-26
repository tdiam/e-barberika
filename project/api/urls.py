from django.urls import path

from project.token_auth.views import LoginView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='api-login'),
    path('logout/', LogoutView.as_view(), name='api-logout')
]
