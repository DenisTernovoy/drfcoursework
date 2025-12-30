from django.db import models

from users.models import User


class Habit(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        null=True,
        blank=True,
    )
    place = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время")
    action = models.CharField(max_length=255, verbose_name="Действие")
    pleasant_habit = models.BooleanField(verbose_name="Приятная привычка")
    linked_habit = models.ForeignKey(
        "self",
        models.SET_NULL,
        verbose_name="Связанная привычка",
        blank=True,
        null=True,
    )
    periodicity = models.IntegerField(default=1, verbose_name="Периодичность в дн.")
    reward = models.CharField(
        max_length=255, verbose_name="Вознаграждение", null=True, blank=True
    )
    complete_time = models.TimeField(verbose_name="Время на выполнение")

    publish = models.BooleanField(verbose_name="Признак публичности", default=True)

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return f"Я буду {self.action} в {self.time} в {self.place}"
