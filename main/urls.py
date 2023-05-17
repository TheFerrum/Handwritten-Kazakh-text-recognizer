from django.urls import path
from . import views

appname ='main'
urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('save-canvas/', views.save_canvas, name='save-canvas'),
    path('predict-canvas/', views.predict_canvas, name='predict-canvas'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile')
]
