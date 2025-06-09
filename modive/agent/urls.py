from django.urls import path
from .views import GenerateWeeklyFeedback, GenerateCustomReport, CreateSession, Test

urlpatterns = [
    path('weekly', GenerateWeeklyFeedback.as_view(), name='weekly'),
    path('chat', GenerateCustomReport.as_view(), name='chat'),
    path('new', CreateSession.as_view(), name='new_session'),
    path('test', Test.as_view(), name='test'),
]