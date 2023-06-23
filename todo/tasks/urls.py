from django.urls import path

from .views import done_state_view, form_view, list_view


app_name = "bookmarkman"
urlpatterns = [
    path("", list_view, name="list"),
    path("add/", form_view, name="add"),
    path("<int:pk>/", form_view, name="edit"),
    path(
        "done/<int:pk>/",
        done_state_view,
        name="done",
        kwargs={"done_state": True},
    ),
    path(
        "not_done/<int:pk>/",
        done_state_view,
        name="not_done",
        kwargs={"done_state": False},
    ),
]
