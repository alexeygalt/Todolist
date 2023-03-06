from django.shortcuts import render
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from bot.models import TgUser
from bot.serializers import TgUserVerCodSerializer


class TgUserUpdate(generics.UpdateAPIView):
    model = TgUser
    serializer_class = TgUserVerCodSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ('patch',)

    def get_object(self):
        try:
            obj = self.model.objects.get(verification_code=self.request.data.get('verification_code'))
        except self.model.DoesNotExist:
            raise ValidationError({'verification_code': 'Неправильный верификационный код'})

        return obj

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
