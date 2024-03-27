"""
URL configuration for Le_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('litereview', include('litereview.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

import litereview.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("litereview/", include("litereview.urls")),
    path("", litereview.views.index_page, name="home"),
    path(
        "login/",
        LoginView.as_view(
            template_name="litereview/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("signup/", litereview.views.signup_page, name="signup"),
    path("logout/", litereview.views.logout_page, name="logout"),
    path("flux", litereview.views.feed_page, name="flux"),
    path("post", litereview.views.posts_page, name="post"),
    path("ticket", litereview.views.ticket_page, name="ticket"),
    path("review", litereview.views.review_page, name="review"),
    path("subscription", litereview.views.follower_page, name="subscription"),
    path("unfollow", litereview.views.unfollow_page, name="unfollow"),
    path("modify", litereview.views.modify_page, name="modify"),
    path("block", litereview.views.block_page, name="block"),
    path("delete_post", litereview.views.delete_post, name="delete_post"),
    path("reply", litereview.views.reply_page, name="replyticket"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
