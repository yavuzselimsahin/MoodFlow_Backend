from django.db import models
from authentication.models import CustomUser

class TimeEntry(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DurationField()
    ticket_name = models.CharField(max_length=255)
    ticket_color = models.CharField(max_length=7)  # Hex color code
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_paused = models.BooleanField(default=False)