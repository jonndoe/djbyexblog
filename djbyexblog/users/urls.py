from django.urls import path

from djbyexblog.users.views import (
    user_redirect_view,
    user_update_view,
    user_detail_view,
    posts_of_user,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path('user/<id>/posts/', posts_of_user, name='posts_of_user'), # see users page with posts listed
]
