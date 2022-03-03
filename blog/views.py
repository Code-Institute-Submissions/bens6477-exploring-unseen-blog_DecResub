from django.shortcuts import render
from django.views import generic
from .models import Article


class ArticleList(generic.ListView):
    model = Article
    queryset = Article.objects.filter(approved=True).order_by('-created_date')
    template_name = 'index.html'
    paginate_by = 6
    