from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from base.models import User, Article, ArticleCategory
from .serializers import ArticleSerializer
from django.conf import settings
from django.db import IntegrityError

import jwt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/token/refresh/',
        '/api/articles/',
        '/api/article/',
    ]

    return Response(routes)

# view to check user access token validity
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def checkToken(request):
    token = request.data['access_token']
    if not token:
        return Response({
            "error": "No token provided"
        }, status=400)

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return Response({"error": "Token has expired"}, status=401)
    except jwt.DecodeError:
        return Response({"error": "Invalid token"}, status=401)

    return Response({
        "user_id": payload["user_id"],
        "username": payload["username"],
    }, status=200)


# register new user
@api_view(['POST'])
def registerUser(request):
    if request.user.is_authenticated:
        # if user is already logged in, return error
        return Response({"error": "Please logout to create a new account."}, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']

        try:
            user = User.objects.create_user(username, email, password)
            user.save()

            return Response({"success": "Account successfully created."}, status=200)
        except IntegrityError:
            return Response({"error": "Account already exists."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET']) # arguments are allowed methods
@permission_classes([IsAuthenticated]) # permission level required
def articles(request):
    if request.method == "GET":
        articles = Article.objects.filter(author=request.user)
        serializer = ArticleSerializer(articles, many=True) # many=True to serialize multiple items

        return Response(serializer.data)


@api_view(['GET', 'POST', 'PUT', 'DELETE']) # arguments are allowed methods
@permission_classes([IsAuthenticated]) # permission level required
def article(request, slug):
    if request.method == "GET":
        try:
            article = Article.objects.filter(author=request.user).get(slug=slug)
            serializer = ArticleSerializer(article)
            return Response(serializer.data)
        
        except Exception as exception:
            return Response({"error": exception})
        
    if request.method == "POST":
        category_name = request.data['category']

        # check if article category already exists
        category = None
        if len(category_name) > 0:
            category, created = ArticleCategory.objects.get_or_create(name=category_name)

        serializer = ArticleSerializer(
            data = {
                "title": request.data["title"],
                "category": category.pk if category else None,
                "author": request.user.id,
                "content": request.data["content"],
                "slug": slug,
            }
        )

        if not serializer.is_valid(raise_exception=True):
            raise ValidationError(serializer.errors)
        
        serializer.save()

        return Response(f"""New article submitted:\n{serializer.data}""")

        # else:
        #     return Response("There was an error handling the request.", status=status.HTTP_400_BAD_REQUEST)
        
