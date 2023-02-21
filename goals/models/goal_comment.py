from django.contrib.auth import get_user_model
from django.db import models

from goals.models.base import DatesModelMixin
from goals.models.goal import Goal

USER_MODEL = get_user_model()


class GoalComment(DatesModelMixin):
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    goal = models.ForeignKey(Goal, verbose_name="Цель", on_delete=models.CASCADE)
    user = models.ForeignKey(USER_MODEL, verbose_name='Автор', on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Текст")

    def __str__(self):
        return f"Комментарий к цели {self.goal}"