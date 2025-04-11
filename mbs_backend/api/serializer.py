from rest_framework import serializers
from .models import User, Movies

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  

class MoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = '__all__'