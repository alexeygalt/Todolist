from django.contrib.auth import get_user_model
from django.db import models
from goals.models.base import DatesModelMixin
from goals.models.goal_category import GoalCategory

USER_MODEL = get_user_model()


class Goal(DatesModelMixin):
    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    class Status(models.IntegerChoices):
        to_do = 1, "К выполнению"
        in_progress = 2, "В процессе"
        done = 3, "Выполнено"
        archived = 4, "Архив"

    class Priority(models.IntegerChoices):
        low = 1, "Низкий"
        medium = 2, "Средний"
        high = 3, "Высокий"
        critical = 4, "Критический"

    user = models.ForeignKey(USER_MODEL, verbose_name='Автор', on_delete=models.CASCADE)
    category = models.ForeignKey(GoalCategory, verbose_name='Категория', on_delete=models.CASCADE,
                                 related_name='goals')
    title = models.CharField(verbose_name="Название", max_length=255)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    status = models.PositiveSmallIntegerField(
        verbose_name='Статус',
        choices=Status.choices,
        default=Status.to_do,
    )
    priority = models.PositiveSmallIntegerField(
        verbose_name='Приоритет',
        choices=Priority.choices,
        default=Priority.medium,
    )
    due_date = models.DateTimeField(verbose_name='Дедлайн', blank=True, null=True)

    def __str__(self):
        return self.title
