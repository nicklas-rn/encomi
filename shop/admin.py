from django.contrib import admin
from .models import Item, Image, Style, StyleGroup, Category, Seller


admin.site.register(Item)
admin.site.register(Image)
admin.site.register(Style)
admin.site.register(StyleGroup)
admin.site.register(Category)
admin.site.register(Seller)

