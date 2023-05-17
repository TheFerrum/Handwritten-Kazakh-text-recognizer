from django.shortcuts import render, redirect
from .models import News
from .forms import NewsForm
from django.views.generic import DetailView, UpdateView, DeleteView

def news_home(request):
    news = News.objects.order_by('-date')
    return render(request, 'news/news_home.html', {'news':news})

class NewsDetailsView(DetailView):
    model = News
    template_name = 'news/details_view.html'
    context_object_name = 'article'

class NewsUpdateView(UpdateView):
    model = News
    template_name = 'news/create.html'

    # fields = ['title', 'anons', 'ful_text', 'date']
    form_class = NewsForm

class NewsDeleteView(DeleteView):
    model = News
    success_url = '/news/'
    template_name = 'news/news_delete.html'

def news_create(request):
    error=''
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Form is not valid'
    form = NewsForm()

    data = {
        'form': form,
        'error': error
    }
    return render(request, 'news/create.html',data)