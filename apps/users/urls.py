from django.urls import path
from .views import GoogleLoginSignupView

urlpatterns = [
    path('google/login', GoogleLoginSignupView.as_view()),
]
