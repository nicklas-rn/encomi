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
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('help/<seller_name>', views.help, name='help'),
    path('help_faqs/<seller_name>/<type>', views.help_faqs, name='help_faqs'),


    path('dashboard/home/<seller_name>', views.dashboard, name='dashboard'),
    path('dashboard/listings/<seller_name>', views.listings, name='listings'),
    path('dashboard/deliveries/<order_id>/<seller_name>', views.deliveries, name='deliveries'),
    path('dashboard/settings/<seller_name>', views.settings, name='settings'),
    path('dashboard/listings_items/<seller_name>', views.listings_items, name='listings_items'),
    path('dashboard/listings_new/<seller_name>', views.listings_new, name='listings_new'),
    path('dashboard/listings_new_customization_group/<id>/<seller_name>', views.listings_new_customization_group, name='listings_new_customization_group'),
    path('dashboard/listings_new_customization_option/<id>/<count>/<seller_name>', views.listings_new_customization_option,
         name='listings_new_customization_option'),
    path('dashboard/listings_new_image/<seller_name>', views.listings_new_image, name='listings_new_image'),
    path('dashboard/listings_new_save/<seller_name>', views.listings_new_save, name='listings_new_save'),
    path('dashboard/deliveries_selected/<seller_name>/<order_id>', views.deliveries_selected, name='deliveries_selected'),
    path('dashboard/update_order_status/<seller_name>/<order_id>/<order_status>', views.update_order_status,
         name='update_order_status'),
    path('dashboard/update_settings_content/<seller_name>/<content>', views.update_settings_content,
         name='update_settings_content'),
    path('dashboard/create_settings_faq/<seller_name>', views.create_settings_faq,
         name='create_settings_faq'),
    path('dashboard/delete_settings_faq/<seller_name>', views.delete_settings_faq,
         name='delete_settings_faq'),

    path('seller_policy/<seller_name>', views.seller_policy, name='seller_policy'),
    path('privacy_policy/<seller_name>', views.privacy_policy, name='privacy_policy'),
    path('TOU/<seller_name>', views.TOU, name='TOU'),
    path('about/<seller_name>', views.about, name='about'),

    path('scrape/<seller_name>', views.scrape, name='scrape')


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)