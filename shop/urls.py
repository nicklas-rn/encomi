from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('item/<id>', views.item, name='item'),
    path('cart/', views.cart, name='cart'),
    path('cart_preview/', views.cart_preview, name='cart_preview'),
    path('shop_items/', views.shop_items, name='shop_items')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)