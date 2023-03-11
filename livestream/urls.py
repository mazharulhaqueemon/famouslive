from django.urls import path
from .views import CreateActiveCallsView
from fcm.views import AgoraRtcTokenRetrieveApiView
urlpatterns = [
    path('live-streaming-state-update/', CreateActiveCallsView.as_view()),
    path('agora-rtc-token-retrieve/',AgoraRtcTokenRetrieveApiView.as_view()),
]