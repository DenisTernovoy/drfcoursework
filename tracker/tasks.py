import json
from datetime import datetime, timedelta

import requests
from celery import shared_task
from django.utils import timezone
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from config import settings
from tracker.models import Habit


@shared_task
def create_periodic_habit(
    id_habit: int, periodicity: int, chat_id: str, time: datetime.time
) -> None:
    """Создание периодической задачи на основе созданной привычки"""

    if chat_id:
        # базовая дата — сегодня
        today = timezone.localdate()  # или date.today()
        dt = datetime.combine(today, time) - timedelta(hours=1)

        if datetime.now() >= dt:
            dt += timedelta(days=1)

        """Создаем интервал для повтора"""
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=periodicity,
            period=IntervalSchedule.DAYS,
        )

        # Создаем задачу для повторения
        PeriodicTask.objects.create(
            interval=schedule,
            name=f"Привычка {id_habit}",
            task="tracker.tasks.send_telegram_notification",
            kwargs=json.dumps({"id_habit": id_habit, "chat_id": chat_id}),
            start_time=dt,
        )


@shared_task
def send_telegram_notification(id_habit: int, chat_id: str) -> None:
    """Отправка сообщения в телеграм пользователю о напоминании выполнить привычку"""

    habit = str(Habit.objects.get(pk=id_habit))
    data = {
        "chat_id": chat_id,
        "text": f"Через 1 час мне нужно выполнить следующую привычку:\n{habit}",
    }

    url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"

    requests.post(url, data=data)
