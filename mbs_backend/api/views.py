from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail, EmailMessage
from rest_framework import status
from datetime import date
from .models import User, Movies, Payment, Home_page, Order, Ticket
from .serializer import HomePageSerializer
from .serializer import PaymentSerializer
from .serializer import MoviesSerializer
from .serializer import UserSerializer
from .serializer import TicketSerializer, OrderSerializer
import qrcode
import os

@api_view(['GET'])
def get_users(request):
    users =  User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(UserSerializer(serializer.data, many=True).data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_user(request):
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')

    if not first_name or not last_name:
        return Response(
            {"error": "First name and last name are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password = request.data.get('password')

        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        
        if password:
            user.set_password(password)

        if not any([first_name, last_name, password]):
            return Response(
                {"error": "At least one field (first_name, last_name, or password) is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST', 'PUT'])  # Add PUT to the allowed methods
def movies(request, pk=None):
    if request.method == 'GET':
        if pk: 
            try:
                movie = Movies.objects.get(pk=pk)
                serializer = MoviesSerializer(movie)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Movies.DoesNotExist:
                return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)

        title = request.query_params.get('title', None)
        genre = request.query_params.get('genre', None)
        movies = Movies.objects.all()
        if title:
            movies = movies.filter(title__icontains=title)
        if genre:
            movies = movies.filter(genre__icontains=genre)
        serializer = MoviesSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST': 
        serializer = MoviesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        try:
            movie = Movies.objects.get(pk=pk)
        except Movies.DoesNotExist:
            return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get data from request
        title = request.data.get('title')
        release_date = request.data.get('release_date')
        genre = request.data.get('genre')
        director = request.data.get('director')
        poster_url = request.data.get('poster_url')

        # Update only provided fields
        if title:
            movie.title = title
        if release_date:
            movie.release_date = release_date
        if genre:
            movie.genre = genre
        if director:
            movie.director = director
        if poster_url:
            movie.poster_url = poster_url

        # Validate that at least one field is being updated
        if not any([title, release_date, genre, director, poster_url]):
            return Response(
                {"error": "At least one field must be provided for update."},
                status=status.HTTP_400_BAD_REQUEST
            )

        movie.save()
        serializer = MoviesSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def now_playing(request):
    today = date.today()
    movies = Movies.objects.filter(release_date__lte=today)
    serializer = MoviesSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def upcoming_movies(request):
    today = date.today()
    movies = Movies.objects.filter(release_date__gt=today)
    serializer = MoviesSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def payment_checkout(request):
    try:
        # Validate required fields
        required_fields = ['user', 'method', 'amount', 'movie', 'show_time']
        for field in required_fields:
            if field not in request.data:
                return Response(
                    {"error": f"Missing required field: {field}"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Get user instance first
        try:
            user = User.objects.get(id=request.data['user'])
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Create payment with user instance
        payment_data = {
            'user': user.id,  # Use user.id here
            'method': request.data['method'],
            'amount': request.data['amount'],
            'status': 'PENDING',
            'transaction_id': request.data.get('transaction_id', None)
        }

        serializer = PaymentSerializer(data=payment_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        payment = serializer.save()

        # Create order after payment
        order = Order.objects.create(
            user=user,
            movie=request.data['movie'],
            total_price=payment.amount
        )

        # Create ticket
        ticket = Ticket.objects.create(
            order=order,
            show_time=request.data['show_time']
        )

        # Generate QR code data
        qr_data = (
            f"Ticket ID: {ticket.id}\n"
            f"Order ID: {order.id}\n"
            f"Movie: {order.movie}\n"
            f"Show Time: {ticket.show_time}\n"
            f"User: {order.user.email}"
        )
        
        # Generate and save QR code
        qr_image = qrcode.make(qr_data)
        qr_code_path = f"media/qr_codes/ticket_{ticket.id}.png"
        os.makedirs(os.path.dirname(qr_code_path), exist_ok=True)
        qr_image.save(qr_code_path)

        # Update ticket with QR code path
        ticket.qr_code_path = qr_code_path
        ticket.save()

        # Prepare email content
        email_body = f"""
        Thank you for your purchase!

        Order Details:
        Movie: {order.movie}
        Show Time: {ticket.show_time}
        Amount Paid: ${payment.amount}

        Your ticket is attached to this email.
        Please present the QR code at the theater entrance.

        Enjoy the movie!
        """

        # Send confirmation email
        try:
            email = EmailMessage(
                subject='Movie Ticket Confirmation',
                body=email_body,
                from_email="noreply@moviebooking.com",
                to=[payment.user.email],
            )
            email.attach_file(qr_code_path)
            email.send()
        except Exception as e:
            print(f"Email sending failed: {str(e)}")

        # Return success response with order details
        response_data = {
            "message": "Payment processed successfully",
            "order": {
                "id": order.id,
                "movie": order.movie,
                "total_price": str(order.total_price),
                "ticket": {
                    "id": ticket.id,
                    "show_time": ticket.show_time,
                    "qr_code_url": f"/media/qr_codes/ticket_{ticket.id}.png"
                },
                "payment": {
                    "status": payment.status,
                    "transaction_id": payment.transaction_id
                }
            }
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {"error": str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def payment_confirm(request):
     transaction_id = request.GET.get('transaction_id')
     try:
         payment = Payment.objects.get(transaction_id=transaction_id)
         payment.status = 'COMPLETED'
         payment.save()
         return Response({"message": "Payment confirmed successfully and ticket issued."}, status=status.HTTP_200_OK)
     except Payment.DoesNotExist:
         return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def payment_third_party(request):
    serializer = PaymentSerializer(data=request.data)
    if serializer.is_valid():
        payment = serializer.save()
        return Response({"message": "Payment processed successfully."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def payment_methods(request):
    methods = [method[1] for method in Payment.PAYMENT_METHODS]
    return Response(methods, status=status.HTTP_200_OK)

@api_view(['GET'])
def home_page(request):
    home_page = Home_page.objects.all()
    serializer = HomePageSerializer(home_page, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK) 

@api_view(['GET'])
def order_history(request):
    user_id = request.query_params.get('user_id')

    if not user_id:
        return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    orders = Order.objects.filter(user_id=user_id)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def order_detail(request, id):
    try:
        order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def ticket_detail(request, id):
    try:
        ticket = Ticket.objects.get(id=id)
    except Ticket.DoesNotExist:
        return Response({"error": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = TicketSerializer(ticket)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def user_tickets(request):
    user_id = request.query_params.get('user_id')

    if not user_id:
        return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    tickets = Ticket.objects.filter(user_id=user_id)
    serializer = TicketSerializer(tickets, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)