from django.shortcuts import render, reverse, redirect, get_object_or_404, get_list_or_404
from django.views import generic, View
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from .models import Article, Country
from .forms import ArticleForm, CountryForm, CommentForm


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


class ArticleAdd(View):
    def get(self, request, country_name):        
        country = get_object_or_404(Country, country_name=country_name)
        articles = list(Article.objects.all())
        form = ArticleForm()
        context = {"form": form}
        return render(request, "add_article.html", context)

    def post(self, request, country_name):
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
    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        articles = list(Article.objects.all())
        form = ArticleForm(instance=article)
        context = {
            "form": form,
            "article": article,
        }
        return render(request, "edit_article.html", context)


class ArticleUpvote(View):
    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        if article.upvotes.filter(id=request.user.id).exists():
            article.upvotes.remove(request.user)
        else:
            article.upvotes.add(request.user)
            if article.downvotes.filter(id=request.user.id).exists():
                article.downvotes.remove(request.user)
        
        return HttpResponseRedirect(reverse('article_detail', args=[slug]))


class ArticleDownvote(View):
    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        if article.downvotes.filter(id=request.user.id).exists():
            article.downvotes.remove(request.user)
        else:
            article.downvotes.add(request.user)
            if article.upvotes.filter(id=request.user.id).exists():
                article.upvotes.remove(request.user)
        
        return HttpResponseRedirect(reverse('article_detail', args=[slug]))


class Countries(View):
    def get(self, request):
        countries = Country.objects.all().filter(approve_country=True)
        context = {'countries': countries}
        return render(request, 'countries.html', context)


class CountryArticles(View):
    def get(self, request, country_name, *args, **kwargs):
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
    def get(self, request):
        countries = list(Country.objects.all())
        form = CountryForm()
        context = {"form": form}
        return render(request, "add_country.html", context)
        
    def post(self, request):
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
    def get(self, request, country_name):
        country = get_object_or_404(Country, country_name=country_name)
        countries = list(Country.objects.all())
        form = CountryForm(instance=country)
        context = {"form": form}
        return render(request, "edit_country.html", context)
        
    def post(self, request, country_name):
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
    def get(self, request, country_name):
        country = get_object_or_404(Country, country_name=country_name)
        country.delete()
        return redirect('countries')
