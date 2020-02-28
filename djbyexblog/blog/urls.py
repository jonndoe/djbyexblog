from django.urls import path
from . import views


app_name = "blog"
urlpatterns = [
    path(
        route='',
        view=views.BlogListView.as_view(),
        name='list',
    ),

]
