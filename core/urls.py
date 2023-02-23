from django.urls import path

from core.views import UserRegistrationView, UserLoginView, UserRetrieveUpdateDestroyView, PasswordUpdateView

urlpatterns = [
    path('signup', UserRegistrationView.as_view(), name='signup'),
    path('login', UserLoginView.as_view(), name='login'),
    path('profile', UserRetrieveUpdateDestroyView.as_view(), name='profile'),
    path('update_password', PasswordUpdateView.as_view(), name='update_password'),
]
