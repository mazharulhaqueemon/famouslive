from rest_framework import generics
from .serializer import ActiveCallsSerializer
from .models import ActiveCall

class CreateActiveCallsView(generics.CreateAPIView):
    serializer_class = ActiveCallsSerializer

    def perform_create(self, serializer):
        active_calls_data = serializer.validated_data.get('active_calls', [])
        for call_data in active_calls_data:
            call = ActiveCall.objects.create(**call_data)

# Create your views here.
