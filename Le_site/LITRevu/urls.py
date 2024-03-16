from django.urls import path
from . import views
from .views import HomeView
from django.contrib.auth import views as auth_views

app_name ='LiTRevu'
urlpatterns = [
    # path('', views.home, name="home"),
    path('', HomeView.as_view(),name="home"),
    path('login/', auth_views.LoginView.as_view(), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),


]