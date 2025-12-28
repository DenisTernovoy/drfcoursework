from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from tracker.models import Habit
from tracker.paginators import HabitPaginator
from tracker.permissions import IsOwner
from tracker.serializers import HabitSerializer
from tracker.tasks import create_periodic_habit


class HabitViewSet(ModelViewSet):
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator

    def perform_create(self, serializer):
        instance = serializer.save(owner=self.request.user)

        create_periodic_habit.delay(
            instance.pk, instance.periodicity, instance.owner.chat_id, instance.time
        )

    def get_queryset(self):
        queryset = Habit.objects.filter(Q(owner=self.request.user) | Q(publish=True))
        return queryset

    def get_permissions(self):
        if self.action == "list":
            self.permission_classes = [
                IsAuthenticated,
            ]
        else:
            self.permission_classes = [IsOwner, IsAuthenticated]

        return super().get_permissions()
