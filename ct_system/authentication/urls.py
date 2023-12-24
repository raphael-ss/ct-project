from django.urls import path
from .views import Registration, ValidateUsername, ValidateEmail, LoginView, LogoutView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register', Registration.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('validate-username', csrf_exempt(ValidateUsername.as_view()), name='validate-username'),
    path('validate-email', csrf_exempt(ValidateEmail.as_view()), name="validate-email"),
]