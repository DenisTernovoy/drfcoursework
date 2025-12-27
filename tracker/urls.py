from rest_framework import routers

from tracker import views
from tracker.apps import TrackerConfig

app_name = TrackerConfig.name

router = routers.DefaultRouter()
router.register(r"habits", views.HabitViewSet, basename="habits")

urlpatterns = [] + router.urls
