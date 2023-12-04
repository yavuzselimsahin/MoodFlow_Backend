from rest_framework import serializers
from .models import Note
from bs4 import BeautifulSoup
from django.utils.html import strip_tags
from textblob import TextBlob

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'


    def create(self, validated_data):
        body_html = validated_data.pop('body_html', '')
        soup = BeautifulSoup(body_html, 'html.parser')
        plain_text = strip_tags(soup.get_text(separator=' '))

        blob = TextBlob(plain_text)
        sentiment = blob.sentiment.polarity

        if sentiment > 0.6:
            mood = 'joy'
        elif sentiment > 0.2 and sentiment < 0.6:
            mood = 'surprise'
        elif sentiment >= 0 and sentiment < 0.2:
            mood = 'fear'
        elif sentiment > -0.2 and sentiment < 0:
            mood = 'fear'
        elif sentiment > -0.4 and sentiment < -0.2:
            mood = 'anger'
        elif sentiment < -0.4:
            mood = 'sadness'
        else:
            mood = 'neutral'

        validated_data['mood'] = mood

        # Save the plain text in the 'body' field
        validated_data['body'] = plain_text

        # Save the HTML content in the 'body_html' field
        validated_data['body_html'] = body_html

        # Create the Note instance
        instance = Note.objects.create(**validated_data)

        return instance    


    def update(self, instance, validated_data):
        body_html = validated_data.pop('body_html', '')
        soup = BeautifulSoup(body_html, 'html.parser')
        plain_text = strip_tags(soup.get_text(separator=' '))

        # Save the plain text in the 'body' field
        instance.body = plain_text

        # Save the HTML content in the 'body_html' field
        instance.body_html = body_html

        if 'title' in validated_data:
            instance.title = validated_data['title']

        blob = TextBlob(plain_text)
        sentiment = blob.sentiment.polarity

        if sentiment > 0.6:
            instance.mood = 'joy'
        elif sentiment > 0.2 and sentiment < 0.6:
            instance.mood = 'surprise'
        elif sentiment >= 0 and sentiment < 0.2:
            instance.mood = 'fear'
        elif sentiment > -0.2 and sentiment < 0:
            instance.mood = 'fear'
        elif sentiment > -0.4 and sentiment < -0.2:
            instance.mood = 'anger'
        elif sentiment < -0.4:
            instance.mood = 'sadness'
        else:
            instance.mood = 'neutral'

        # Update the Note instance
        instance.save()

        return instance

