from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('item/<id>', views.item, name='item'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart_preview/', views.cart_preview, name='cart_preview'),
    path('cart_total/', views.cart_total, name='cart_total'),
    path('shop_items/', views.shop_items, name='shop_items'),

    path('become_seller/', views.become_seller, name='become_seller'),
    path('dashboard/home/', views.dashboard, name='dashboard'),

    path('scrape/', views.scrape, name='scrape')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)