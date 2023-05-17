from django.urls import path
from . import views
urlpatterns = [
     path('view/', views.view_images, name='view_images')
]
