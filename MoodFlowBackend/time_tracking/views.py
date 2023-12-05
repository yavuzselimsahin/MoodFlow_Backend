from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .models import TimeEntry
from .serializers import TimeEntrySerializer
from django.utils import timezone
from rest_framework.decorators import action, api_view
from rest_framework.response import Response



@permission_classes([IsAuthenticated])
class TimeEntryListCreateView(generics.ListCreateAPIView):
    serializer_class = TimeEntrySerializer

    def get_queryset(self):
        return TimeEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        start_time = timezone.now()
        end_time = serializer.validated_data['end_time']
        duration = end_time - start_time
        serializer.save(user=self.request.user, duration=duration, start_time=start_time)

@permission_classes([IsAuthenticated])
class TimeEntryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TimeEntrySerializer

    def get_queryset(self):
        return TimeEntry.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        time_entry = self.get_object()
        time_entry.duration = time_entry.end_time - time_entry.start_time
        time_entry.save()
        return response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pause_time_entry(request, pk):
    try:
        time_entry = TimeEntry.objects.get(pk=pk, user=request.user)
    except TimeEntry.DoesNotExist:
        return Response({'status': 'Time entry not found'}, status=status.HTTP_404_NOT_FOUND)

    if not time_entry.is_paused:
        time_entry.is_paused = True
        time_entry.duration = timezone.now() - time_entry.start_time
        time_entry.save()
        return Response({'status': 'Time entry paused'})
    else:
        return Response({'status': 'Time entry already paused'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def continue_time_entry(request, pk):
    try:
        time_entry = TimeEntry.objects.get(pk=pk, user=request.user)
    except TimeEntry.DoesNotExist:
        return Response({'status': 'Time entry not found'}, status=status.HTTP_404_NOT_FOUND)

    if time_entry.is_paused:
        time_entry.is_paused = False
        time_entry.start_time = timezone.now()
        time_entry.save()
        return Response({'status': 'Time entry continued'})
    else:
        return Response({'status': 'Time entry not paused'}, status=status.HTTP_400_BAD_REQUEST)