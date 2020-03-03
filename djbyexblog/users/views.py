from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from djbyexblog.app_posts.models import Post

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):
    fields = ['name',"bio",]

    # We already imported user in the View code above,
    #   remember?
    model = User

    # Send the User Back to Their Own Page after a 
    #   successful Update
    def get_success_url(self):
        return reverse('users:detail',
            kwargs={
                'username': \
                self.request.user.username}
                
        )

    def get_object(self):
        # Only Get the User Record for the 
        #   User Making the Request
        return User.objects.get(
            username=self.request.user.username)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})




@login_required
def posts_of_user(request, id):
    user = get_object_or_404(User,
                             id=id,
                             is_active=True)

    user_posts = Post.objects.filter(owner=user.id)
    #assert False
    return  render(request,
                   'registration/user/detail.html',
                   {'section': 'people',
                    'user': user,
                    'user_posts': user_posts})


user_redirect_view = UserRedirectView.as_view()
