from django.urls import path
from .views import Registration

urlpatterns = [
    path('register', Registration.as_view(), name="registration")
]