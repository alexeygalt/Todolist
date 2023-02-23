from django.contrib.auth import get_user_model
from django.db import models

from .base import DatesModelMixin

USER_MODEL = get_user_model()


class GoalCategory(DatesModelMixin):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    title = models.CharField(verbose_name='Название', max_length=255)
    user = models.ForeignKey(USER_MODEL, verbose_name='Автор', on_delete=models.CASCADE)
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)

    def __str__(self):
        return self.title
