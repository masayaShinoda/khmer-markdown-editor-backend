from django.db import models
from django.contrib.auth.models import User
import markdown
from django.template.defaultfilters import slugify


class ArticleCategory(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author", null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(max_length=64, default="", unique=True)

    def __str__(self):
        return self.title

    def formatted_markdown(self):
        return markdown.markdown(self.content)