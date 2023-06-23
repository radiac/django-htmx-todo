from typing import Any

from django.shortcuts import get_object_or_404, redirect, render

from .forms import TaskForm
from .models import Task


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
    return render(request, "tasks/list.html", context=context)


def form_view(request, pk: int | None = None):
    task = None if pk is None else get_object_or_404(Task, pk=pk)
    context: dict[str, Any] = {
        "task": task,
    }

    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        context["task"] = form.save()
        return redirect("tasks:list")
    else:
        context["form"] = form
        return render(request, "tasks/form.html", context=context)


def done_state_view(request, pk: int, done_state: bool):
    task = get_object_or_404(Task, pk=pk)
    if task.done != done_state:
        task.done = done_state
        task.save()

    return render(
        request,
        "tasks/done_state.html",
        context={
            "task": task,
        },
    )
