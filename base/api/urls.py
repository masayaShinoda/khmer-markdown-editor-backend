from django.urls import path
from . import views
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('', views.getRoutes),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'), # custom token pair view
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('check-token/', views.checkToken),
    path('register/', views.registerUser),
    path('articles/', views.articles),  
    path('article/', views.article),
    path('article/<int:id>/', views.article),
    path('article/slug/<str:slug>/', views.articleBySlug), # return article matching slug
]
