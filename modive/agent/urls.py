from django.urls import path
from .views import TestView, GenerateWeeklyFeedback

urlpatterns = [
    path('test', TestView.as_view(), name='test'),
    path('weekly', GenerateWeeklyFeedback.as_view(), name='weekly'),
]