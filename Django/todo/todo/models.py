from django.db import models

# Create your models here.
class ToDo(models.Model):
    title = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now=True, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title