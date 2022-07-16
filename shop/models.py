from django.db import models


class Item(models.Model):
    title = models.CharField(max_length=30)
    keywords = models.CharField(blank=True, null=True, max_length=120)

    def __str__(self):
        return self.title
