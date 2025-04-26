from rest_framework import serializers
from .models import User, Movies, Home_page, Payment, Order, Ticket

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
        fields = ['id', 'user', 'method', 'amount', 'status', 'transaction_id']

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'show_time', 'seat_number', 'qr_code_path', 'status']

class OrderSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer(read_only=True)
    payment = PaymentSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user_id', 'movie', 'purchase_date', 'total_price', 'ticket', 'payment']

