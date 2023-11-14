from datetime import timezone
from datetime import datetime,timezone
import uuid
from rest_framework import serializers
from notes.serializers import NoteSerializer
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['username'] = user.username
        token['email'] = user.email

        return token

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password2', 'bio', 'display_name', 'cover_photo')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            bio=validated_data['bio'],
            display_name=validated_data['display_name'],
            cover_photo=validated_data['cover_photo']
        )

        user.set_password(validated_data['password'])
        user.save()

        # token = RefreshToken.for_user(user)
        
        # token['username'] = user.username
        # token['email'] = user.email

        return user
          
        
        

class UserSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = '__all__'