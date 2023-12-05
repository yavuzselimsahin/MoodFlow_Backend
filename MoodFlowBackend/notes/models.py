import uuid
from django.db import models
from authentication.models import CustomUser

# Create your models here.
# Model for Notes
MOOD_CHOICES = [
    ('joy', 'Joy'),
    ('anger', 'Anger'),
    ('trust', 'Trust'),
    ('fear', 'Fear'),
    ('surprise', 'Surprise'),
    ('sadness', 'Sadness'),
    ('disgust', 'Disgust'),
    ('anticipation', 'Anticipation'),
    ('neutral', 'Neutral')
    ]
class Note(models.Model):
    body = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=40, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES, default='neutral')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='notes')
    body_html = models.TextField(null=True, blank=True,)
    def __str__(self):
        return self.title