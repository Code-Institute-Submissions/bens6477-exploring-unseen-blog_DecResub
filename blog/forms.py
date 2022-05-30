from .models import Article, Country, Comment
from django import forms


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'image', 'summary', 'attraction')


class CountryForm(forms.ModelForm):
    class Meta: 
        model = Country
        fields = ('country_name',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        
