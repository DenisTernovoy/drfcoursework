from rest_framework.serializers import ValidationError


class HabitValidator:
    def __init__(
        self, linked_habit, reward, complete_time, pleasant_habit, periodicity
    ):
        self.linked_habit = linked_habit
        self.reward = reward
        self.complete_time = complete_time
        self.pleasant_habit = pleasant_habit
        self.periodicity = periodicity

    def __call__(self, value):
        linked_habit = dict(value).get(self.linked_habit)
        reward = dict(value).get(self.reward)
        complete_time = dict(value).get(self.complete_time)
        pleasant_habit = dict(value).get(self.pleasant_habit)
        periodicity = dict(value).get(self.periodicity)

        if reward and linked_habit:
            raise ValidationError(
                "Необходимо указать что-то одно: вознаграждение или связанную привычку"
            )

        if complete_time:
            if int(complete_time) >= 120:
                raise ValidationError(
                    "Время выполнения должно быть не больше 120 секунд"
                )

        if linked_habit:
            if not linked_habit.pleasant_habit:
                raise ValidationError(
                    "В связанные привычки могут попадать только привычки с признаком приятной привычки"
                )

        if pleasant_habit:
            if reward or linked_habit:
                raise ValidationError(
                    "У приятной привычки не может быть вознаграждения или связанной привычки"
                )

        if periodicity:
            if int(periodicity) > 7:
                raise ValidationError(
                    "Нельзя выполнять привычку реже, чем 1 раз в 7 дней"
                )
