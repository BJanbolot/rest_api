from django.urls import path
from .views import RegisterView, LoginView, ActivationView, UserListAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginView.as_view()),
    path('activation/', ActivationView.as_view()),
    path('users/', UserListAPIView.as_view()),

]