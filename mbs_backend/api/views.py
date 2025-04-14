from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Movies, shows
from .serializer import MoviesSerializer
from .serializer import UserSerializer
from .serializer import showsSerializer

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
def get_shows(request):
    shows = shows.object.all()
    serializer = showsSerializer(data=request.data)
    return Response(showsSerializer(serializer.data, many=True).data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_shows(request):
    serializer = showsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

