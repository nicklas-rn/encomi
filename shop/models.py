from django.db import models


class Image(models.Model):
    image = models.ImageField(upload_to="media/item_images")

    def __str__(self):
        return self.image.name


class Item(models.Model):
    title = models.CharField(max_length=30)
    keywords = models.CharField(blank=True, null=True, max_length=120)
    images = models.ManyToManyField(Image)

    def __str__(self):
        return self.title
