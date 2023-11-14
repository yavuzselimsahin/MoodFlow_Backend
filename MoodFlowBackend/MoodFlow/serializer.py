from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ('full_name', 'email', 'phone_number') 
        fields = '__all__'