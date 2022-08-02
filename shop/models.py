from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(upload_to="item_images")
    item = models.ForeignKey('Item', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.image.name


class Item(models.Model):
    title = models.CharField(max_length=1200)
    keywords = models.CharField(blank=True, null=True, max_length=1200, default='All')
    price = models.FloatField(blank=True, null=True)
    old_price = models.FloatField(blank=True, null=True)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title


class StyleGroup(models.Model):
    type = models.CharField(max_length=30)
    item = models.ForeignKey('Item', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.type


class Style(models.Model):
    title = models.CharField(max_length=30)
    price = models.FloatField(null=True, blank=True)
    style_group = models.ForeignKey('StyleGroup', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

