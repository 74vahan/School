from django.urls import path

from .views import LessonListView

urlpatterns = [path("", LessonListView.as_view(), name="schedule")]
