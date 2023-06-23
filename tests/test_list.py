import pytest

from todo.tasks.models import Task


pytestmark = pytest.mark.django_db


def test_task_list(client):
    task = Task.objects.create(label="test task 1", done=False)

    response = client.get("/")
    assert task in response.context["tasks"]
    assert task.label in str(response.content)
