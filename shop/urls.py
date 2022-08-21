from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('home/<seller_name>', views.home, name='home'),
    path('shop/<seller_name>', views.shop, name='shop'),
    path('item/<seller_name>/<id>', views.item, name='item'),
    path('cart/<seller_name>', views.cart, name='cart'),
    path('checkout/<seller_name>', views.checkout, name='checkout'),
    path('cart_preview/<seller_name>', views.cart_preview, name='cart_preview'),
    path('cart_total/<seller_name>', views.cart_total, name='cart_total'),
    path('shop_items/<seller_name>', views.shop_items, name='shop_items'),

    path('become_seller/', views.become_seller, name='become_seller'),
    path('dashboard/home/<seller_name>', views.dashboard, name='dashboard'),
    path('dashboard/listings/<seller_name>', views.listings, name='listings'),
    path('dashboard/deliveries/<seller_name>', views.deliveries, name='deliveries'),
    path('dashboard/settings/<seller_name>', views.settings, name='settings'),

    path('seller_policy', views.seller_policy, name='seller_policy'),
    path('privacy_policy', views.privacy_policy, name='privacy_policy'),
    path('TOU', views.TOU, name='TOU'),
    path('about/', views.about, name='about'),

    path('scrape/', views.scrape, name='scrape')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)