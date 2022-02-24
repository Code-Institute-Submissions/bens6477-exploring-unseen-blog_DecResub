from django.contrib import admin
from .models import Article, Country
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = ('content')

admin.site.register(Country)
