from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Movies
from .serializer import MoviesSerializer
from .serializer import UserSerializer

@api_view(['GET'])
def get_users(request):
    users =  User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(UserSerializer(serializer.data, many=True).data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_user(request):
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

@api_view(['GET'])
def get_movies(request):
    movies =  Movies.objects.all()
    serializer = MoviesSerializer(movies, many=True)
    return Response(MoviesSerializer(serializer.data, many=True).data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_movie(request):
    serializer = MoviesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)