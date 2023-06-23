from django.contrib.admin import site

from .models import Task


site.register(Task)
