from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticlesForm
from django.views.generic import DetailView, UpdateView, DeleteView

def articles_home(request):
    articles = Article.objects.order_by('-date')
    return render(request, 'articles/articles_home.html', {'articles':articles})

class ArticlesDetailsView(DetailView):
    model = Article
    template_name = 'articles/details_view.html'
    context_object_name = 'article'

class NewsUpdateView(UpdateView):
    model = Article
    template_name = 'articles/create.html'

    # fields = ['title', 'anons', 'ful_text', 'date']
    form_class = ArticlesForm

class NewsDeleteView(DeleteView):
    model = Article
    success_url = '/articles/'
    template_name = 'articles/articles_delete.html'

def articles_create(request):
    error=''
    if request.method == 'POST':
        form = ArticlesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Form is not valid'
    form = ArticlesForm()

    data = {
        'form': form,
        'error': error
    }
    return render(request, 'articles/create.html',data)