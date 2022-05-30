from . import views
from django.urls import path

urlpatterns = [
    path('', views.ArticleList.as_view(), name='home'),
    path('countries/', views.Countries.as_view(), name='countries'),
    path('country/add/', views.CountryAdd.as_view(), name="add_country"),
    path('country/add/<slug:country_name>/', views.CountryEdit.as_view(), name="edit_country"),
    path('countries/<slug:country_name>/', views.CountryArticles.as_view(), name='country_articles'),
    path('<slug:slug>/', views.ArticleDetail.as_view(), name='article_detail'),
    path('upvote/<slug:slug>/', views.ArticleUpvote.as_view(), name='article_upvote'),
    path('downvote/<slug:slug>/', views.ArticleDownvote.as_view(), name="article_downvote"),
    path('article/add/<slug:country_name>/', views.ArticleAdd.as_view(), name="add_article")
]