from django.shortcuts import render, reverse, redirect, get_object_or_404, get_list_or_404
from django.views import generic, View
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from .models import Article, Country
from .forms import ArticleForm, CountryForm, CommentForm


class ArticleList(generic.ListView):
    """
    Gets a list of all approved articles
    """
    model = Article
    queryset = Article.objects.filter(approved=True).order_by('-created_date')
    template_name = 'index.html'
    paginate_by = 6


class ArticleDetail(View):
    """
    Handles methods concerning a specific article by filtering by its slug.
    """
    def get(self, request, slug, *args, **kwargs):
        """
        Gets a specific article by filtering by its slug and returns
        whether the user has up/downvoted article
        """
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
        """
        Posts user comments to a specific article by filtering by its slug
        """
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


class ArticleAdd(View):
    """
    Adds new article
    """
    def get(self, request, country_name):
        """
        Renders add_article template and creates a new article form
        """
        country = get_object_or_404(Country, country_name=country_name)
        articles = list(Article.objects.all())
        form = ArticleForm()
        context = {"form": form}
        return render(request, "add_article.html", context)

    def post(self, request, country_name):
        """
        Renders add_article template and edits a specified article form
        """
        country = get_object_or_404(Country, country_name=country_name)
        articles = list(Article.objects.all())
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            form.instance.country = country
            summernote = request.POST.get("editordata")
            form.instance.content = summernote
            for article in articles:
                form.instance.attraction = request.POST.get("attraction")
                form.instance.summary = request.POST.get("summary")

                name = form.instance.title
                if article.title == name:
                    messages.add_message(
                        request,
                        messages.INFO,
                        "An article with the same title already exists.",
                    )
                    context = {"form": form}
                    return render(request, "add_article.html", context)

            form.instance.slug = form.instance.title.replace(" ", "-").lower()
            form.save()
            messages.add_message(
                request, messages.INFO, "Your article is awaiting approval"
            )
            queryset = Article.objects.all().filter(approved=True, country__country_name=country_name)
            article_queryset = get_list_or_404(queryset)
            return render(
                request,
                "country_articles.html",
                {
                    "articles": article_queryset,
                    "country_name": country
                }   
            )
        context = {"form": form}
        return render(request, "add_article.html", context)


class ArticleEdit(View):
    """
    Edits specified article
    """
    def get(self, request, slug):
        """
        Renders edit_article template and edits a specified article form
        """
        article = get_object_or_404(Article, slug=slug)
        articles = list(Article.objects.all())
        form = ArticleForm(instance=article)
        context = {
            "form": form,
            "article": article,
            "slug": article.slug,
        }
        return render(request, "edit_article.html", context)

    def post(self, request, slug):
        """
        Renders edit_article template and posts a specified article form
        """
        article = get_object_or_404(Article, slug=slug)
        country_name = article.country
        country = get_object_or_404(Country, country_name=country_name)
        articles = list(Article.objects.all())
        form = ArticleForm(instance=article)
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.instance.author = request.user
            form.instance.country = country
            summernote = request.POST.get("editordata")
            form.instance.content = summernote
            form.instance.attraction = request.POST.get("attraction")
            form.instance.summary = request.POST.get("summary")
            form.instance.slug = form.instance.title.replace(" ", "-").lower()
            form.save()
            queryset = Article.objects.all().filter(approved=True, country__country_name=country_name)
            article_queryset = get_list_or_404(queryset)
            return render(
                request,
                "country_articles.html",
                {
                    "articles": article_queryset,
                    "country_name": country
                }   
            )
        context = {
            "form": form,
            "article": article,
            "slug": article.slug,
            }
        return render(request, "edit_article.html", context)


class ArticleDelete(View):
    """
    Deletes a specified article
    """
    def get(self, request, slug):
        """
        Deletes a specified article
        """
        article = get_object_or_404(Article, slug=slug)
        country_name = article.country
        articles = list(Article.objects.all())
        article.delete()
        return render(
            request,
            "country_articles.html",
            {
                "articles": articles,
                "country_name": country
            }   
        )


class ArticleUpvote(View):
    """
    Upvotes specified article
    """
    def post(self, request, slug):
        """
        Upvotes specified article
        """
        article = get_object_or_404(Article, slug=slug)
        if article.upvotes.filter(id=request.user.id).exists():
            article.upvotes.remove(request.user)
        else:
            article.upvotes.add(request.user)
            if article.downvotes.filter(id=request.user.id).exists():
                article.downvotes.remove(request.user)
        
        return HttpResponseRedirect(reverse('article_detail', args=[slug]))


class ArticleDownvote(View):
    """
    Downvotes specified article
    """
    def post(self, request, slug):
        """
        Downvotes specified article
        """
        article = get_object_or_404(Article, slug=slug)
        if article.downvotes.filter(id=request.user.id).exists():
            article.downvotes.remove(request.user)
        else:
            article.downvotes.add(request.user)
            if article.upvotes.filter(id=request.user.id).exists():
                article.upvotes.remove(request.user)
        
        return HttpResponseRedirect(reverse('article_detail', args=[slug]))


class Countries(View):
    """
    Gets a list of all approved articles
    """
    def get(self, request):
        """
        Gets a list of all approved articles then renders countries page
        """
        countries = Country.objects.all().filter(approve_country=True)
        context = {'countries': countries}
        return render(request, 'countries.html', context)


class CountryArticles(View):
    """
    Gets a list of all approved articles for specified country
    """
    def get(self, request, country_name, *args, **kwargs):
        """
        Gets a list of all approved articles for specified country
        """
        queryset = Article.objects.all().filter(approved=True, country__country_name=country_name)
        articles = get_list_or_404(queryset)
        return render(
            request,
            "country_articles.html",
            {
                "articles": articles,
                "country_name": country_name
            }   
        )


class CountryAdd(View):
    """
    Adds new country
    """
    def get(self, request):
        """
        Renders add_country template and adds a new country form
        """
        countries = list(Country.objects.all())
        form = CountryForm()
        context = {"form": form}
        return render(request, "add_country.html", context)
        
    def post(self, request):
        """
        Renders add_country template and posts a new country form
        """
        countries = list(Country.objects.all())
        form = CountryForm(request.POST)
        if form.is_valid():
            # form.instance.category_author = request.user
            for country in countries:
                name = form.instance.country_name
                if country.country_name == name:
                    messages.add_message(
                        request,
                        messages.INFO,
                        "A country with the same name already exists.",
                    )
                    context = {"form": form}
                    return render(request, "add_country.html", context)
            form.save()
            messages.add_message(
                request, messages.INFO, "Your country is awaiting approval"
            )
            return redirect("countries")
        
        context = {"form": form}
        return render(request, "add_country.html", context)


class CountryEdit(View):
    """
    Edits new country
    """
    def get(self, request, country_name):
        """
        Renders edit_country template and adds a new country form
        """
        country = get_object_or_404(Country, country_name=country_name)
        countries = list(Country.objects.all())
        form = CountryForm(instance=country)
        context = {"form": form}
        return render(request, "edit_country.html", context)
        
    def post(self, request, country_name):
        """
        Renders edit_country template and edits a specified country form
        """
        country = get_object_or_404(Country, country_name=country_name)
        countries = list(Country.objects.all())
        form = CountryForm(request.POST, instance=country)
        if form.is_valid():
            for country in countries:
                name = form.instance.country_name
                if country.country_name == name:
                    messages.add_message(
                        request,
                        messages.INFO,
                        "A country with the same name already exists.",
                    )
                    context = {"form": form}
                    return render(request, "edit_country.html", context)
            form.save()
            messages.add_message(
                request, messages.INFO, "Your country is awaiting approval"
            )
            return redirect("countries")
        
        context = {"form": form}
        return render(request, "edit_country.html", context)


class CountryDelete(View):
    """
    Deletes a specified country
    """
    def get(self, request, country_name):
        """
        Deletes a specified country
        """
        country = get_object_or_404(Country, country_name=country_name)
        country.delete()
        return redirect('countries')
