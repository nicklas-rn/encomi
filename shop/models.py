from django.db import models


class Image(models.Model):
    image = models.ImageField(upload_to="item_images")

    def __str__(self):
        return self.image.name


class Style(models.Model):
    title = models.CharField(max_length=30)
    price = models.FloatField()

    def __str__(self):
        return self.title


class StyleGroup(models.Model):
    type = models.CharField(max_length=30)
    styles = models.ManyToManyField(Style)

    def __str__(self):
        return self.type


class Item(models.Model):
    title = models.CharField(max_length=30)
    keywords = models.CharField(blank=True, null=True, max_length=120)
    images = models.ManyToManyField(Image)
    style_groups = models.ManyToManyField(StyleGroup)
    price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.title
