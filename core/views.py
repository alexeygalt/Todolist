import json

from django.contrib.auth import authenticate, login, get_user, logout
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import User
from core.serializers import UserRegistrationSerializer, UserLoginSerializer, UserRetrieveUpdateSerializer, \
    UserChangePasswordSerializer


class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


@method_decorator(csrf_exempt, name="dispatch")
class UserLoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        if username in [None, '']:
            return JsonResponse({"username": ["Введите Имя пользователя"]}, status=status.HTTP_400_BAD_REQUEST)
        password = data.get('password')
        if password in [None, '']:
            return JsonResponse({"password": ["Введите пароль"]}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return JsonResponse(UserLoginSerializer(User).data)
        return JsonResponse({'error': 'Invalid login'}, status=status.HTTP_404_NOT_FOUND)


class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        obj = get_user(self.request)
        return obj

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response(status=204)


class PasswordUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        obj = get_user(self.request)
        return obj


