from django.urls import path
from .views import GoogleLoginSignupView

urlpatterns = [
    path('', GoogleLoginSignupView.as_view()),
]