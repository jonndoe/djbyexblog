from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Post


class BlogListView(ListView):
    model = Post

