from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.exceptions import ValidationError
from base.models import Article, ArticleCategory
from .serializers import ArticleSerializer, ArticleCategorySerializer

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
        '/api/token',
        '/api/token/refresh'
    ]

    return Response(routes)

@api_view(['GET']) # arguments are allowed methods
def getArticles(request):
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True) # many=True to serialize multiple items
    
    return Response(serializer.data)

@api_view(['GET'])
def getArticleCategories(request):
    article_categories = ArticleCategory.objects.all()
    serializer = ArticleCategorySerializer(article_categories, many=True)

    return Response(serializer.data)

@api_view(['POST'])
def addArticle(request):
    category_name = request.data['category']

    # check if article category exists, if not return error
    category = ArticleCategory.objects.get(name=category_name)
    if category is not None:
        serializer = ArticleSerializer(
            data = {
                "title": request.data["title"],
                "category": category.pk,
                "content": request.data["content"],
            }
        )

        if not serializer.is_valid(raise_exception=True):
            raise ValidationError(serializer.errors)
        
        serializer.save()

        return Response(f"""New article submitted:\n{serializer.data}""")

    else:
        return Response("There was an error", status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def addPost(request):
#     category_name = request.data.get('category')
#     category = Category.objects.get(name=category_name)
#     serializer = PostSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save(category=category)
#     return Response(serializer.data)