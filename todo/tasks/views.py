from functools import wraps
from typing import Any

from django.shortcuts import get_object_or_404, redirect, render

from .forms import TaskForm
from .models import Task


def check_htmx(fn):
    """
    Decorator to check if the request is from htmx, and add a flag to the request if it
    is.

    For function-based views like this, this would normally be done in middleware,
    probably using django-htmx.

    For class-based views you'd probably then want to add a check to get_template_name()
    and then pick up partial_template_name from a class attribute
    """

    @wraps(fn)
    def is_htmx(request, *args, **kwargs):
        # htmx sets the HX-Request header to "true" when it's initiating the request
        if request.headers.get("HX-Request", "false") == "true":
            request.is_htmx = True
        else:
            request.is_htmx = False
        return fn(request, *args, **kwargs)

    return is_htmx


@check_htmx
def list_view(request):
    qs = Task.objects.all()

    filter_done: bool | None
    match request.GET.get("done"):
        case "true":
            filter_done = True
            qs = qs.done()
        case "false":
            filter_done = False
            qs = qs.not_done()
        case _:
            filter_done = None

    context: dict[str, Any] = {
        "tasks": qs,
        "filter_done": filter_done,
    }
    return render(
        request,
        template_name=(
            # If this came from htmx render the partial template, otherwise render the
            # full template - which inherits from base.html and includes the partial.
            "tasks/partials/list.html"
            if request.is_htmx
            else "tasks/list.html"
        ),
        context=context,
    )


@check_htmx
def form_view(request, pk: int | None = None):
    task = None if pk is None else get_object_or_404(Task, pk=pk)
    context: dict[str, Any] = {
        "task": task,
    }

    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        context["task"] = form.save()

        # Normally when you submit a form you want to send the user on to a new page
        # with a redirect to avoid refresh re-submissions. If the request comes from
        # htmx, we can just return a render of the new task
        if request.is_htmx:
            return render(request, "tasks/partials/list-task.html", context=context)
        else:
            return redirect("tasks:list")
    else:
        context["form"] = form

        return render(
            request,
            template_name=(
                "tasks/partials/list-form.html"
                if request.is_htmx
                else "tasks/form.html"
            ),
            context=context,
        )


@check_htmx
def done_state_view(request, pk: int, done_state: bool):
    task = get_object_or_404(Task, pk=pk)
    if task.done != done_state:
        task.done = done_state
        task.save()

    return render(
        request,
        template_name=(
            "tasks/partials/list-task.html"
            if request.is_htmx
            else "tasks/done_state.html"
        ),
        context={
            "task": task,
        },
    )
