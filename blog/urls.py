from . import views
from django.urls import path

urlpatterns = [
    path('', views.ArticleList.as_view(), name='home'),
    path('<slug:slug>/', views.ArticleDetail.as_view(), name='article_detail'),
    path('upvote/<slug:slug>/', views.ArticleUpvote.as_view(), name='article_upvote'),
    path('downvote/<slug:slug>/', views.ArticleDownvote.as_view(), name="article_downvote")
]