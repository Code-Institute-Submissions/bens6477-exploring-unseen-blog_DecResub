from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch
from .models import Article, Country


class TestModels(TestCase):

    def test_approved_defaults_to_false(self):
        self.user = User.objects.create(username='fake')
        self.country = Country.objects.create(
            country_name='Fake',
            approve_country=True)
        self.article = Article.objects.create(
            title='Third Test Article',
            slug='third-test-article',
            country_id=1, author_id=1,
            attraction='Third Test Article',
            summary='Summary',
            content='Content')
        self.assertFalse(self.article.approved)
    
    def test_article_string_method_returns_title(self):
        self.user = User.objects.create(username='fake')
        self.country = Country.objects.create(
            country_name='Fake',
            approve_country=True)
        self.article = Article.objects.create(
            title='Third Test Article',
            slug='third-test-article',
            country_id=1, author_id=1,
            attraction='Third Test Article',
            summary='Summary',
            content='Content')
        self.assertEqual(str(self.article), 'Third Test Article')