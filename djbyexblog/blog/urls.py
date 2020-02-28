from django.urls import path
from . import views


app_name = "blog"
urlpatterns = [
    path(
        route='',
        view=views.PostListView.as_view(),
        name='list',
    ),
    path(
        route='<int:year>/<int:month>/<int:day>/<slug:post>/',
        view=views.PostDetailView.as_view(),
        name='detail',
    ),

]
