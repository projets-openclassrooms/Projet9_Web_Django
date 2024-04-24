from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, DetailView, ListView

from .models import Review, Ticket


class Index(ListView):
    model = Ticket
    queryset = model.objects.all().order_by("time_created")
    template_name = "litereview/index.html"
    paginate_by = 1


class Featured(ListView):
    model = Review
    queryset = model.objects.filter(featured=True).order_by("-time_created")
    template_name = "litereview/featured.html"
    paginate_by = 1


class DetailArticleView(DetailView):
    model = Ticket
    template_name = "litereview/blog_post.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DetailArticleView, self).get_context_data(*args, **kwargs)
        context["followed_user"] = False
        article = Ticket.objects.get(id=self.kwargs.get("pk"))
        if article.likes.filter(pk=self.request.user.id).exists():
            context["followed_user"] = True
        return context


class LikeArticle(View):
    def post(self, request, pk):
        article = Review.objects.get(id=pk)
        if article.likes.filter(pk=self.request.user.id).exists():
            article.likes.remove(request.user.id)
        else:
            article.likes.add(request.user.id)

        article.save()
        return redirect("detail_article", pk)


class DeleteArticleView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ticket
    template_name = "litereview/blog_delete.html"
    success_url = reverse_lazy("index")

    def test_func(self):
        article = Ticket.objects.get(id=self.kwargs.get("pk"))
        return self.request.user.id == article.author.id
