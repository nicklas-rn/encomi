from django.contrib import admin
from .models import *


admin.site.register(Item)
admin.site.register(Image)
admin.site.register(Style)
admin.site.register(StyleGroup)
admin.site.register(Category)
admin.site.register(Seller)
admin.site.register(ParentOrder)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderItemStyleGroup)
admin.site.register(User)
admin.site.register(SellerApplication)
admin.site.register(FAQ)
admin.site.register(HelpMessage)
admin.site.register(NewsletterEmail)

