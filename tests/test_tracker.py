from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from tracker.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    """Тестирование модели привычки"""

    def setUp(self) -> None:
        super().setUp()

        self.user = User.objects.create(email="admin@admin.com", password=12345)

        self.habit_pleasant = Habit.objects.create(
            place="Улица",
            time="15:00:00",
            action="Прогуляться",
            pleasant_habit=True,
            periodicity=1,
            complete_time=100,
            publish=True,
            owner=self.user,
        )

        self.habit = Habit.objects.create(
            place="Дом",
            time="15:00:00",
            action="Уборка",
            pleasant_habit=False,
            periodicity=1,
            complete_time=100,
            publish=True,
            owner=self.user,
        )

        self.client.force_authenticate(user=self.user)

    def test_create_pleasant_habit(self) -> None:
        """Тестирование создания привычки"""

        url = reverse("tracker:habits-list")

        data = {
            "place": "Спортзал",
            "time": "12:00:00",
            "action": "Делать упражнения",
            "pleasant_habit": False,
            "periodicity": 1,
            "complete_time": 100,
            "publish": True,
            "linked_habit": self.habit_pleasant.pk,
        }

        response = self.client.post(url, data=data)
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(result.get("place"), data["place"])

    def test_retrieve_pleasant_habit(self) -> None:
        """Тестирование получения объекта привычки"""

        url = reverse("tracker:habits-detail", args=(self.habit_pleasant.pk,))

        response = self.client.get(url)
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(result.get("place"), self.habit_pleasant.place)

        self.assertEqual(
            str(self.habit_pleasant), "Я буду Прогуляться в 15:00:00 в Улица"
        )

    def test_patch_pleasant_habit(self) -> None:
        """Тестирование изменения объекта привычки"""

        url = reverse("tracker:habits-detail", args=(self.habit_pleasant.pk,))

        data = {
            "periodicity": 3,
            "publish": False,
        }

        response = self.client.patch(url, data=data)
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(result.get("periodicity"), data["periodicity"])

        self.assertEqual(result.get("publish"), data["publish"])

    def test_destroy_pleasant_habit(self) -> None:
        """Тестирование удаления объекта привычки"""

        url = reverse("tracker:habits-detail", args=(self.habit_pleasant.pk,))

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_validator_reward(self):
        """Тестирование валидатора по полям reward и linked_habit"""

        url = reverse("tracker:habits-list")

        data = {
            "place": "Спортзал",
            "time": "12:00:00",
            "action": "Делать упражнения",
            "pleasant_habit": False,
            "periodicity": 1,
            "complete_time": 100,
            "publish": True,
            "linked_habit": self.habit_pleasant.pk,
            "reward": "Скушать пирожок",
        }

        response = self.client.post(url, data=data)

        result = response.json()

        self.assertRaises(ValidationError)

        self.assertEqual(
            result.get("non_field_errors")[0],
            "Необходимо указать что-то одно: вознаграждение или связанную привычку",
        )

    def test_validator_complete_time(self):
        """Тестирование валидатора по полю complete_time"""

        url = reverse("tracker:habits-list")

        data = {
            "place": "Спортзал",
            "time": "12:00:00",
            "action": "Делать упражнения",
            "pleasant_habit": False,
            "periodicity": 1,
            "complete_time": 140,
            "publish": True,
            "linked_habit": self.habit_pleasant.pk,
        }

        response = self.client.post(url, data=data)
        result = response.json()

        self.assertRaises(ValidationError)

        self.assertEqual(
            result.get("non_field_errors")[0],
            "Время выполнения должно быть не больше 120 секунд",
        )

    def test_validator_linked_habit(self):
        """Тестирование валидатора по полю linked_habit"""

        url = reverse("tracker:habits-list")

        data = {
            "place": "Спортзал",
            "time": "12:00:00",
            "action": "Делать упражнения",
            "pleasant_habit": False,
            "periodicity": 8,
            "complete_time": 100,
            "publish": True,
            "linked_habit": self.habit.pk,
        }

        response = self.client.post(url, data=data)
        result = response.json()

        self.assertRaises(ValidationError)

        self.assertEqual(
            result.get("non_field_errors")[0],
            "В связанные привычки могут попадать только привычки с признаком приятной привычки",
        )

    def test_validator_pleasant_habit(self):
        """Тестирование валидатора по полю pleasant_habit"""

        url = reverse("tracker:habits-list")

        data = {
            "place": "Спортзал",
            "time": "12:00:00",
            "action": "Делать упражнения",
            "pleasant_habit": True,
            "periodicity": 1,
            "complete_time": 100,
            "publish": True,
            "linked_habit": self.habit_pleasant.pk,
        }

        response = self.client.post(url, data=data)
        result = response.json()

        self.assertRaises(ValidationError)

        self.assertEqual(
            result.get("non_field_errors")[0],
            "У приятной привычки не может быть вознаграждения или связанной привычки",
        )

    def test_validator_periodicity(self):
        """Тестирование валидатора по полю periodicity"""

        url = reverse("tracker:habits-list")

        data = {
            "place": "Спортзал",
            "time": "12:00:00",
            "action": "Делать упражнения",
            "pleasant_habit": False,
            "periodicity": 8,
            "complete_time": 100,
            "publish": True,
            "linked_habit": self.habit_pleasant.pk,
        }

        response = self.client.post(url, data=data)
        result = response.json()

        self.assertRaises(ValidationError)

        self.assertEqual(
            result.get("non_field_errors")[0],
            "Нельзя выполнять привычку реже, чем 1 раз в 7 дней",
        )
