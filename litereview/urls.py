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

from django.contrib.auth.views import LoginView
from django.urls import path
from django.views.generic import RedirectView

import litereview.views

# import litereview.tests

urlpatterns = [
    # path("", litereview.views.index_page, name="login"),
    path("index/", litereview.views.index_page, name="home"),
    path("signup/", litereview.views.signup_page, name="signup"),
    path(
        "login/",
        LoginView.as_view(
            template_name="litereview/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    # path("registered", litereview.views.home_page, name="registered"),
    path("logout/", litereview.views.logout_page, name="logout"),
    path("flux", litereview.views.feed_page, name="flux"),
    # path("testing", litereview.tests.test_testing, name="testing"),
    path("posts", litereview.views.posts_page, name="posts"),
    path("ticket", litereview.views.ticket_page, name="ticket"),
    # Create
    path(
        "create_ticket/<int:ticket_id>", litereview.views.modify_ticket, name="modify_ticket"
    ),
    path("review/", litereview.views.review_page, name="review"),
    # path("modify", litereview.views.modify_page, name="modify"),
    path(
        "create-ticket/<str:ticket_id>",
        litereview.views.modify_ticket,
        name="create-ticket",
    ),
    path(
        "create_review/<str:ticket_id>",
        litereview.views.review_page_update,
        name="create_review",
    ),
    #Delete
    path(
        "delete-review/<str:ticket_id>",
        litereview.views.delete_review,
        name="delete-review",
    ),
    path("delete_post", litereview.views.delete_post, name="delete_post"),

    #Update
    path(
        "review_page_update/<str:ticket_id>",
        litereview.views.review_page_update,
        name="review_page_update",
    ),
    path(
        "update_review/<str:review_id>",
        litereview.views.update_review_page,
        name="update_review_page",
    ),

    path("block/<str:blocked_user_id>", litereview.views.block_page, name="block"),
    path("subscription", litereview.views.follower_page, name="subscription"),
]

urlpatterns += [
    path("", RedirectView.as_view(url="login/", permanent=True)),
]
