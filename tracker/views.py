from django.db.models import Q
from rest_framework.viewsets import ModelViewSet

from tracker.models import Habit
from tracker.serializers import HabitSerializer


class HabitViewSet(ModelViewSet):
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        instance = serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = Habit.objects.filter(Q(owner=self.request.user) | Q(publish=True))
        return queryset
