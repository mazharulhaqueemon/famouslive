from django.urls import path
from .views import CreateActiveCallsView
urlpatterns = [
    path('live-streaming-state-update/', CreateActiveCallsView.as_view()),

]