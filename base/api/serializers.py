from rest_framework import serializers
from base.models import Article

class ArticleSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Article
        fields = '__all__'