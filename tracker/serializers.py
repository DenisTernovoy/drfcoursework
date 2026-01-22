from rest_framework import serializers

from tracker.models import Habit
from tracker.validators import HabitValidator


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            HabitValidator(
                "linked_habit",
                "reward",
                "complete_time",
                "pleasant_habit",
                "periodicity",
            )
        ]
