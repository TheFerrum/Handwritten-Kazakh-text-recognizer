from django.urls import path
from . import views
urlpatterns = [
     path('view/', views.view_images, name='view_images'),
     path('view/<int:image_id>/', views.view_image, name='view_image'),
     path('delete-image/', views.delete_image, name='delete_image'),
]
