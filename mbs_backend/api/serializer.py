from rest_framework import serializers
from .models import User, Movies, Home_page, Payment

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

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'