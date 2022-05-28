from django.contrib import admin
from .models import Article, Country, Comment
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('country_name', 'approve_country')
    search_fields = ['country_name']
    actions = ['approve_country']

    def approve_country(self, request, queryset):
        queryset.update(approve_country=True)


@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = (
        'title', 'country', 'created_date',
        'updated_date', 'approved')
    list_filter = ('approved', 'created_date')
    search_fields = ['title', 'content']
    summernote_fields = ('content')
    actions = ['approve_article']

    def approve_article(self, request, queryset):
        queryset.update(approved=True)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('body', 'user_name', 'article', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ['body', 'article']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
