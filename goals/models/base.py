from django.db import models


class DatesModelMixin(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата последнего обновления")
