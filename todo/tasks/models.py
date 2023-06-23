from django.db import models


class TaskQuerySet(models.QuerySet):
    def done(self):
        return self.filter(done=True)

    def not_done(self):
        return self.filter(done=False)


class Task(models.Model):
    label = models.CharField(max_length=255)
    done = models.BooleanField(default=False)

    objects = TaskQuerySet.as_manager()
