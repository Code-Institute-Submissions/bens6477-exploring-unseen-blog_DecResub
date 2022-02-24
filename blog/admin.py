from django.contrib import admin
from .models import Article, Country, Comment
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('approved', 'created_date')
    list_display = ('title', 'country', 'created_date', 'updated_date', 'approved')
    search_fields = ['title', 'content']
    summernote_fields = ('content')

admin.site.register(Country)
