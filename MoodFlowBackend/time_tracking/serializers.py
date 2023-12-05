from rest_framework import serializers
from .models import TimeEntry

class TimeEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeEntry
        fields = ['id','created_at', 'start_time', 'end_time', 'duration', 'ticket_name', 'ticket_color', 'user', 'is_paused']
        read_only_fields = ['id', 'original_start_time', 'start_time', 'duration', 'user']