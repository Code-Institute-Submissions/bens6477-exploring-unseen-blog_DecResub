from django.test import TestCase
from django.contrib.auth.models import User
from .models import Article, Country


class TestViews(TestCase):

    def test_get_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    
    def test_get_country_articles_page(self):
        user = User.objects.create(username='fake')
        country = Country.objects.create(
            country_name='Fake',
            approve_country=True)
        article = Article.objects.create(
            title='Third Test Article',
            slug='third-test-article',
            country_id=1, author_id=1,
            attraction='Third Test Article',
            summary='Summary',
            content='Content',
            approved=True)
        response = self.client.get(f'/countries/{country.country_name}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'country_articles.html')
    
    def test_get_country_page(self):
        response = self.client.get('/countries/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'countries.html')
    
    # def test_get_add_country_page(self):
    #     pass
    
    # def test_get_edit_country_page(self):
    #     pass

    def test_get_article_detail_page(self):
        user = User.objects.create(username='fake')
        country = Country.objects.create(
            country_name='Fake',
            approve_country=True)
        article = Article.objects.create(
            title='Third Test Article',
            slug='third-test-article',
            country_id=1, author_id=1,
            attraction='Third Test Article',
            summary='Summary',
            content='Content',
            approved=True)
        response = self.client.get(f'/{article.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'article_detail.html')
    
    # def test_get_add_article_page(self):
    #     pass
    
    # def test_get_edit_article_page(self):
    #     pass