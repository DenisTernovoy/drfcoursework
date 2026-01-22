from typing import Any

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from tracker.models import Habit
from tracker.paginators import HabitPaginator
from tracker.permissions import IsOwner
from tracker.serializers import HabitSerializer
from tracker.tasks import create_periodic_habit


class HabitViewSet(ModelViewSet):
    """Вьюсет для модели привычки"""

    serializer_class = HabitSerializer
    pagination_class = HabitPaginator

    def perform_create(self, serializer) -> None:
        """Переопредление создания объекта модели"""

        instance = serializer.save(owner=self.request.user)

        create_periodic_habit.delay(
            instance.pk, instance.periodicity, instance.owner.chat_id, instance.time
        )

    def get_queryset(self):
        """Получение QuerySet модели привычки"""

        queryset = Habit.objects.filter(owner=self.request.user)
        return queryset

    def get_permissions(self) -> Any:
        """Переопределение получения списка разрешений"""

        if self.action == "list":
            self.permission_classes = [
                IsAuthenticated,
            ]
        else:
            self.permission_classes = [IsOwner, IsAuthenticated]

        return super().get_permissions()


class HabitListAPIView(ListAPIView):
    """Эндпоинт для списка публичных привычек"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(publish=True)
