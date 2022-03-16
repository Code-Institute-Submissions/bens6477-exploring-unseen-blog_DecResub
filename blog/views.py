from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Article
from .forms import CommentForm


class ArticleList(generic.ListView):
    model = Article
    queryset = Article.objects.filter(approved=True).order_by('-created_date')
    template_name = 'index.html'
    paginate_by = 6


class ArticleDetail(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Article.objects.filter(approved=True)
        article = get_object_or_404(queryset, slug=slug)
        comments = article.comments.filter(approved=True).order_by('created_on')
        upvoted = False
        if article.upvotes.filter(id=self.request.user.id).exists():
            upvoted = True
        downvoted = False
        if article.downvotes.filter(id=self.request.user.id).exists():
            downvoted = True
        return render(
            request,
            "article_detail.html",
            {
                "article": article,
                "comments": comments,
                "commented": False,
                "upvoted": upvoted,
                "downvoted": downvoted,
                "comment_form": CommentForm(),
            }   
        )
    
    def post(self, request, slug, *args, **kwargs):
        queryset = Article.objects.filter(approved=True)
        article = get_object_or_404(queryset, slug=slug)
        comments = article.comments.filter(approved=True).order_by('created_on')
        upvoted = False
        if article.upvotes.filter(id=self.request.user.id).exists():
            upvoted = True
        downvoted = False
        if article.downvotes.filter(id=self.request.user.id).exists():
            downvoted = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.user_name = request.user
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.save()
        else:
            comment_form = CommentForm()
        
        return render(
            request,
            "article_detail.html",
            {
                "article": article,
                "comments": comments,
                "commented": True,
                "upvoted": upvoted,
                "downvoted": downvoted,
                "comment_form": comment_form,
            },
        )


class ArticleUpvote(View):
    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        if article.upvotes.filter(id=request.user.id).exists():
            article.upvotes.remove(request.user)
        else:
            article.upvotes.add(request.user)
        
        return HttpResponseRedirect(reverse('article_detail', args=[slug]))
        
