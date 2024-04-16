import copy
import os
from itertools import chain

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.views.decorators.http import require_POST

from Le_site import settings
from litereview import forms
from litereview.models import UserFollows, Review, Ticket, User


# Create your views here.


def index_page(request):
    """
    Log-in view
    """
    form = forms.LogInForm()
    message = ""
    url = "base.html"
    if request.method == "POST":
        form = forms.LogInForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                url = "litereview/home.html"
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                message = "Identifiants invalides"
        else:
            message = "Veuillez entrer un identifiant et un mot de passe."
    return render(request, url, context={"form": form, "message": message})


def signup_page(request):
    form = forms.SignUpForm()
    if request.method == "POST":
        # traitement du formulaire
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, "litereview/signup.html", context={"form": form})


@login_required
def home_page(request):
    # Récupérer les informations de l'utilisateur
    user = request.user

    context = {
        "user": user,

    }
    return render(request, 'litereview/home.html', context)


def logout_page(request):
    logout(request)
    return redirect("login")


def delete_review(request, review_id):
    mydata = User.objects.all().values()
    template = loader.get_template("template.html")
    context = {
        'utilisateurs': mydata,
        'revue': review_id
    }
    return HttpResponse(template.render(context, request))


@login_required
def update_review(request, review_id):
    review = Q(Review.objects.filter(
        Q(review__in=review_id)))
    template = loader.get_template("litereview/partials/replyticket.html")
    form = forms.ReviewForm()
    print("etape 0")
    if request.method == "POST":
        review_form = forms.ReviewForm(request.POST)
        print("etape 1")
        if review_form.is_valid():
            review = review_form.save(commit=False)
            print("etape 0")

            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("posts")
    context = {
        'form': form,
        'review': review
    },
    return render(request, str(template), context=context, )


@login_required
def feed_page(request):
    """
    getting all tickets and their related reviews formatted as such :
    [{ticket: {ticket.values,..},review: {review.values,..}}]
    """
    tickets_with_reviews = []
    followed_users = request.user.follows.all()
    # print(followed_users)
    # Récupérer les tickets et critiques créés par les utilisateurs suivis et l'utilisateur actuel
    reviews = Review.objects.filter(
        Q(user__in=followed_users) | Q(user=request.user)
    )
    tickets = Ticket.objects.filter(
        Q(user__in=followed_users) | Q(user=request.user)
    )
    # form = None

    #
    # form = copy.c
    #
    # opy(forms.FeedForm())
    #     tickets_with_reviews.append({"ticket": ticket, "review": review, "form": form})

    # sorting the list in reverse: most recent first
    # tickets_with_reviews.sort(key=lambda d: d["ticket"].combined_date, reverse=True)
    tickets_with_reviews = sorted(
        chain(reviews, tickets),
        key=lambda instance: instance.time_created,
        reverse=True
    )
    # adds the form component for creating a review

    # if request.method == "POST":
    #     # extract action to do and ticket id
    #     post_value = request.POST.get("post_value")
    #     # post_id is ALWAYS the ticket id
    #     post_id = post_value.split("_")[1]
    #     post_action = post_value.split("_")[0]
    #     print(post_value)
    #     print(post_action)
    #     print(post_id)
    #
    #     # checks the value sent by the post request
    #     if post_action == "update-review":
    #         return redirect("/update-review/" + post_id)
    #
    #     if post_action == "delete-review":
    #         delete_review = Review.objects.get(ticket=post_id)
    #         # only allows to delete own reviews
    #         if delete_review.user == request.user:
    #             delete_review.delete()
    #         return redirect("flux")
    #
    #     if post_action == "delete-ticket":
    #         delete_ticket = Ticket.objects.get(id=post_id)
    #         # only allows to delete own ticket
    #         if delete_ticket.user == request.user:
    #             delete_ticket.delete()
    #         return redirect("flux")
    #
    #     if post_action == "update-review":
    #         review = Review.objects.get(ticket=Ticket.objects.get(id=post_id))
    #         return redirect(f"/create-review/{post_id}/{review.id}")
    #
    #     if post_action == "update-ticket":
    #         return redirect("/create-ticket/" + post_id)
    context = {
        "tickets_with_reviews": tickets_with_reviews,
        # "form": form,
        "user_id": request.user.id,
    }
    # # print('flux')
    # # print(context)
    return render(request, "litereview/flux.html", context=context)


@login_required
def posts_page(request):
    """
    getting all tickets and their related reviews formatted as such :
    [{ticket: {ticket.values,..},review: {review.values,..}}]
    """
    tickets_with_reviews = []
    form = None

    # generates the user list to display
    user_list_filter = [request.user]
    for user_query in UserFollows.objects.filter(user=request.user):
        user_list_filter.append(user_query.followed_user)

    # links reviews data with their ticket
    for ticket in Ticket.objects.filter(user__in=user_list_filter):
        reviews_data = []
        for review in Review.objects.filter(user=request.user, ticket=ticket):
            review_info = {}
            for field in review._meta.get_fields():
                excluded_field = ["id", "ticket"]
                if hasattr(review, field.name) and field.name not in excluded_field:
                    review_info[field.name] = getattr(review, field.name)
            reviews_data.append(review_info)

        ticket.combined_date = ticket.time_created
        ticket.is_open_to_review = True
        review = None
        if reviews_data:
            # adds the original ticket without the review if request.user posted it
            ticket.is_open_to_review = False
            ticket_without_review = copy.copy(ticket)
            tickets_with_reviews.append(
                {"ticket": ticket_without_review, "review": None}
            )

            # keep the first and only review if any
            review = reviews_data[0]
            if review["time_created"] > ticket.time_created:
                ticket.combined_date = review["time_created"]

        if ticket.user != request.user and review is None:
            continue

        form = copy.copy(forms.FeedForm())
        tickets_with_reviews.append({"ticket": ticket, "review": review, "form": form})

    # sorting the list in reverse: most recent first
    tickets_with_reviews.sort(key=lambda d: d["ticket"].combined_date, reverse=True)

    # adds the form component for creating a review

    if request.method == "POST":
        # extract action to do and ticket id
        post_value = request.POST.get("post_value")
        # post_id is ALWAYS the ticket id
        post_id = post_value.split("_")[1]
        post_action = post_value.split("_")[0]
        # checks the value sent by the post request
        if post_action == "create-review":
            return redirect("/create-review/" + post_id)

        if post_action == "delete-review":
            delete_review = Review.objects.get(ticket=post_id)
            # only allows to delete own reviews
            if delete_review.user == request.user:
                delete_review.delete()
            return redirect("posts")

        if post_action == "delete-ticket":
            delete_ticket = Ticket.objects.get(id=post_id)
            # only allows to delete own ticket
            if delete_ticket.user == request.user:
                delete_ticket.delete()
            return redirect("posts")

        if post_action == "update-review":
            review = Review.objects.get(ticket=Ticket.objects.get(id=post_id))
            return redirect(f"/create-review/{post_id}/{review.id}")

        if post_action == "update-ticket":
            return redirect("/create-ticket/" + post_id)

    # print('posts_page')

    context = {
        "tickets_with_reviews": tickets_with_reviews,
        "form": form,
        "user_id": request.user.id,
    }
    # print(context)
    return render(request, "litereview/posts.html", context=context)


@login_required
def follower_page(request):
    follow_form = forms.FollowForm()
    # les abonnements
    followed_user = UserFollows.objects.filter(user=request.user)
    # les abonnes
    followers = UserFollows.objects.filter(followed_user=request.user)
    display_error = None
    # print("here")
    if request.method == "POST":
        post_value = request.POST.get("post_value")
        # print("-1")

        # checks the value sent by the post request
        if post_value == "follow":
            # print("0")
            # recuperation de username et creation d l abonnement
            try:
                followed_user_target = User.objects.get(
                    username=request.POST.get("username")
                )

            except Exception:
                display_error = "Nom d'utilisateur invalide"
                context = {
                    "follow_form": follow_form,
                    "followed_user": followed_user,
                    "followers": followers,
                    "display_error": display_error,
                }
                return render(request, "litereview/abonnement.html", context=context)

            # print("1")
            if followed_user_target == request.user:
                display_error = "Vous ne pouvez pas vous abonner à vous même."
            else:
                try:
                    # print("2")
                    follow = UserFollows()
                    follow.user = request.user
                    follow.followed_user = followed_user_target
                    follow.save()
                except IntegrityError:
                    display_error = "Vous êtes déjà abonné à cet utilisateur"
        else:
            # deletes link with followed_user having 'post_value' username
            unfollow = UserFollows.objects.get(
                user=request.user, followed_user=User.objects.get(username=post_value)
            )
            unfollow.delete()
    else:
        follow_form = forms.FollowForm()

    context = {
        "follow_form": follow_form,
        "followed_user": followed_user,
        "followers": followers,
        "display_error": display_error,
    }

    return render(request, "litereview/abonnement.html", context=context)


@login_required
def ticket_page(request):
    ticket_form = forms.TicketForm()

    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        # print(request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("flux")

    context = {"ticket_form": ticket_form}
    # print(context, 'ticket_page')
    return render(request, "litereview/ticket.html", context=context)
    # @login_required
    # def ticket_page(request):
    #     ticket_form = forms.TicketForm()
    #
    #     if request.method == "POST":
    #         ticket_form = forms.TicketForm(request.POST, request.FILES)
    #         if ticket_form.is_valid():
    #             user, created = request.user.get_or_create(user=user, ticket=ticket_form)
    #             ticket = ticket_form.save(commit=False)
    #             ticket.user = user
    #             ticket.save()
    #             return redirect("feed")


@login_required
def ticket_page_update(request, ticket_id):
    ticket_to_update = Ticket.objects.get(id=ticket_id)
    ticket_form = forms.TicketForm(instance=ticket_to_update)

    if request.method == "POST":
        ticket_form = forms.TicketForm(
            request.POST, request.FILES, instance=ticket_to_update
        )
        if any([ticket_form.is_valid()]):
            ticket_form.save()
            return redirect("feed")

    context = {
        "ticket_form": ticket_form,
        "ticket_values": ticket_id,
        "loaded_image": ticket_to_update.image,
    }
    # print(context, "ticket_page_update")
    return render(request, "litereview/partials/ticket.html", context=context)


@login_required
def review_page(request):
    ticket_form = forms.TicketForm(
        request.POST if request.method == "POST" else None,
        request.FILES if request.method == "POST" else None
    )
    review_form = forms.ReviewForm(
        request.POST if request.method == "POST" else None)
    if (request.method == "POST" and ticket_form.is_valid() and
            review_form.is_valid()):
        ticket = ticket_form.save(commit=False)
        ticket.user = request.user
        review = review_form.save(commit=False)
        review.ticket = ticket
        review.user = request.user
        ticket.save()
        review.save()
        return redirect('home')
    return render(
        request,
        'litereview/review.html',
        context={
            "ticket_form": ticket_form,
            "review_form": review_form,
        }
    )



@login_required
@require_POST
def review_page_update(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    reviews = ticket.review_set.all()
    context = {
        'ticket': ticket,
        'reviews': reviews,
    }
    return render(request, 'litereview/review.html', context)


@login_required
def tickets_reviews_page(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()

    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("feed")

    context = {"ticket_form": ticket_form, "review_form": review_form}
    return render(request, "litereview/partials/tickets-reviews.html", context=context)


@login_required
@require_POST
def unfollow_page(request):
    if request.method == 'POST':
        form = forms.UnfollowForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            user_to_unfollow = User.objects.filter(username=username).first()
            if user_to_unfollow and user_to_unfollow != request.user:
                user_follow = UserFollows.objects.filter(user=request.user, followed_user=user_to_unfollow)
                if user_follow.exists():
                    user_follow.delete()
                    return redirect("subscription")
    return redirect("subscription")


@login_required
@require_POST
def block_page(request):
    block_form = BlockForm(request.POST)
    if block_form.is_valid():
        username = block_form.cleaned_data.get("blocked_user")
        user_to_block = get_object_or_404(User, username=username)

        if user_to_block == request.user:
            return redirect("subscription")

        block_relationship = UserBlocks.objects.filter(user=request.user, blocked_user=user_to_block)

        if block_relationship.exists():
            block_relationship.delete()
        else:
            block = block_form.save(commit=False)
            block.user = request.user
            block.save()

            # Unfollow the user if they were followed
            follow = UserFollows.objects.filter(user=request.user, followed_user=user_to_block)
            follow_back = UserFollows.objects.filter(user=user_to_block, followed_user=request.user)

            if follow.exists():
                follow.delete()
            if follow_back.exists():
                follow_back.delete()

    return redirect("subscription")


@login_required
@require_POST
def delete_post(request):
    # https://docs.djangoproject.com/en/3.1/topics/http/shortcuts/#get-object-or-404

    form = forms.FormDeletepost(request.POST)
    if form.is_valid():
        types = form.cleaned_data["types"]
        postid = form.cleaned_data["postid"]
        if types == "review":
            review = get_object_or_404(Review, id=postid)
            if review.user == request.user:
                review.delete()
        if types == "ticket":
            ticket = get_object_or_404(Ticket, id=postid)
            if ticket.user == request.user:
                if ticket.image:
                    os.remove(ticket.image.path)
                ticket.delete()
    return redirect("posts")


def modify_page(request):
    post_type = request.GET.get("type")
    post_id = request.GET.get("id")

    if post_type == "TICKET":
        return modify_ticket(request, post_id)
    elif post_type == "REVIEW":
        return modify_review(request, post_id)

    return redirect("flux")


def modify_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.user != ticket.user:
        return redirect("flux")

    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
        if ticket_form.is_valid():
            ticket_form.save()
            return redirect("flux")
    else:
        ticket_form = forms.TicketForm(instance=ticket)

    return render(request, "litereview/partials/modify.html", {"ticket": ticket, "ticket_form": ticket_form})


def modify_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect("flux")

    if request.method == "POST":
        review_form = forms.ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review_form.save()
            return redirect("flux")
    else:
        review_form = forms.ReviewForm(instance=review)

    return render(request, "litereview/partials/modify.html", {"review": review, "review_form": review_form})


@login_required
def reply_page(request, post_id):
    if request.method == "POST":

        return process_post_request(request)
    elif request.method == "GET" and "ticket_id" in request.GET:
        return process_get_request(request)
    return redirect("flux")

    context = {"form", form}
    return render(request, "litereview/create-review.html", )


def process_post_request(request):
    ticket_id = request.POST.get("ticket_id")
    ticket = get_object_or_404(Ticket, id=ticket_id)
    review_form = forms.ReviewForm(request.POST)
    if review_form.is_valid():
        review = review_form.save(commit=False)
        review.ticket = ticket
        review.user = request.user
        review.save()
        return redirect("flux")


def process_get_request(request):
    ticket_id = request.GET.get("ticket_id")
    ticket = get_object_or_404(Ticket, id=ticket_id)
    review_form = forms.ReviewForm()
    return render(
        request,
        "litereview/replyticket.html",
        {"review_form": review_form, "ticket": ticket},
    )
