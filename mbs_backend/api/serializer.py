from rest_framework import serializers
from .models import User, Movies, Home_page

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  

class MoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = '__all__'
        
        
class HomePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home_page
        fields = '__all__'