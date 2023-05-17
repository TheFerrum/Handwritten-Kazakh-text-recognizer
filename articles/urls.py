from django.urls import path
from . import views

urlpatterns = [
    path('', views.articles_home, name='articles_home'),
    path('create', views.articles_create, name='articles_create'),
    path('<int:pk>', views.ArticlesDetailsView.as_view(), name='articles-detail'),
    path('<int:pk>/update', views.NewsUpdateView.as_view(), name='articles-update'),
    path('<int:pk>/delete', views.NewsDeleteView.as_view(), name='articles-delete')
]
