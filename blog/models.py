from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Country(models.Model):
    """
    Model for creating Country categories.
    """
    country_name = models.CharField(max_length=100)
    approve_country = models.BooleanField(default=False)

    def __str__(self):
        return self.country_name


class Article(models.Model):
    """
    Model for creating article posts.
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    attraction = models.CharField(max_length=200, unique=True, default="Attraction")
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_articles")
    summary = models.CharField(max_length=250)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    content = models.TextField()
    image = CloudinaryField("image", default="placeholder")
    upvotes = models.ManyToManyField(
        User, related_name="article_upvotes", blank=True)
    downvotes = models.ManyToManyField(
        User, related_name="article_downvotes", blank=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_date']

    def upvote_count(self):
        return self.upvotes.count()

    def downvote_count(self):
        return self.downvotes.count()

    def vote_count(self):
        return self.upvotes.count() - self.downvotes.count()

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Model for creating article comments.
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.body
