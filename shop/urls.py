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
    path('thankyou/<seller_name>', views.thankyou, name='thankyou'),
    path('create_order/<seller_name>', views.create_order, name='create_order'),
    path('cart_preview/<seller_name>', views.cart_preview, name='cart_preview'),
    path('cart_total/<seller_name>', views.cart_total, name='cart_total'),
    path('shop_items/<seller_name>', views.shop_items, name='shop_items'),

    path('become_seller/', views.become_seller, name='become_seller'),
    path('login/', views.login_user, name='login'),
    path('help/<seller_name>', views.help, name='help'),
    path('help_faqs/<seller_name>/<type>', views.help_faqs, name='help_faqs'),


    path('dashboard/home/<seller_name>', views.dashboard, name='dashboard'),
    path('dashboard/listings/<seller_name>', views.listings, name='listings'),
    path('dashboard/deliveries/<order_id>/<seller_name>', views.deliveries, name='deliveries'),
    path('dashboard/settings/<seller_name>', views.settings, name='settings'),
    path('dashboard/listings_items/<seller_name>', views.listings_items, name='listings_items'),
    path('dashboard/deliveries_selected/<seller_name>/<order_id>', views.deliveries_selected, name='deliveries_selected'),
    path('dashboard/update_order_status/<seller_name>/<order_id>/<order_status>', views.update_order_status,
         name='update_order_status'),

    path('seller_policy/<seller_name>', views.seller_policy, name='seller_policy'),
    path('privacy_policy/<seller_name>', views.privacy_policy, name='privacy_policy'),
    path('TOU/<seller_name>', views.TOU, name='TOU'),
    path('about/<seller_name>', views.about, name='about'),

    path('scrape/', views.scrape, name='scrape')


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)