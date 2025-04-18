from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework import status
from datetime import date
from .models import User, Movies, Payment, Home_page
from .serializer import HomePageSerializer
from .serializer import PaymentSerializer
from .serializer import MoviesSerializer
from .serializer import UserSerializer


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
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST'])
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
    serializer = PaymentSerializer(data=request.data)
    if serializer.is_valid():
        payment = serializer.save()

        send_mail(
            subject='Payment Confirmation',
            message=f'Your payment of {payment.amount} has been processed successfully.',
            from_email="noreply@example.com",
            recipient_list=[payment.user.email],
            fail_silently=False,
        )
        return Response({"message": "Payment processed successfully. Confirmation email sent."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

