from django.urls import path

from bot import views

urlpatterns = [
    path('verify', views.TgUserUpdate.as_view()),
]
