import json
from django.shortcuts import render, redirect
from .models import *
from .utils import *
from .scraper import *

# Create your views here.

def base(request):
    return redirect('home/encomi')


def home(request, seller_name):

    cart = cookieCart(request, seller_name)

    seller = Seller.objects.get(name=seller_name)
    print(seller)
    if seller_name != 'encomi':
        items = seller.item_set.all()
    else:
        items = Item.objects.all()

    categories = seller.category_set.all()

    pushed_sellers = Seller.objects.all()


    context = {
        'seller': seller,
        'items': items,
        'cartItems': cart['items'],
        'cartTotal': cart['total'],
        'categories': categories,
        'pushed_sellers': pushed_sellers,
    }

    return render(request, 'shop/home.html', context)


def shop(request, seller_name):
    search = json.loads(request.COOKIES['search'])
    category_id = search['category']
    sort = search['sort']
    keyword = search['keyword']

    cart = cookieCart(request, seller_name)

    seller = Seller.objects.get(name=seller_name)
    if seller_name != 'encomi':

        if category_id != 0:
            try:
                category = seller.category_set.get(id=category_id)
                items = seller.item_set.filter(categories=category)
            except:
                items = seller.item_set.all()
        else:
            items = seller.item_set.all()

    else:
        if category_id != 0:
            try:
                category = seller.category_set.get(id=category_id)
                items = Item.objects.filter(categories=category)
            except:
                items = Item.objects.all()
        else:
            items = Item.objects.all()

    if sort == 'Best':
        items = items.order_by('id')
    elif sort == 'Ascending':
        items = items.order_by('price')
    elif sort == 'Descending':
        items = items.order_by('-price')

    if not keyword == 'all':
        items = items.filter(title__contains=keyword)

    categories = seller.category_set.all()

    """for item in items:
        for style_group in item.style_groups.all():
            print(style_group.type)
            for style in style_group.styles.all():
                print(style.title)
    """

    context = {
        'seller': seller,
        'items': items,
        'categories': categories,
        'cartItems': cart['items'],
        'cartTotal': cart['total'],
    }

    return render(request, 'shop/shop.html', context)


def item(request, seller_name, id):

    cart = cookieCart(request, seller_name)

    item = Item.objects.get(id=id)

    seller = Seller.objects.get(name=seller_name)
    categories = seller.category_set.all()


    context = {
        'seller': seller,
        'item': item,
        'cartItems': cart['items'],
        'cartTotal': cart['total'],
        'categories': categories,
    }

    return render(request, 'shop/item.html', context)


def cart(request, seller_name):
    cart = cookieCart(request, seller_name)

    seller = Seller.objects.get(name=seller_name)


    context = {
        'seller': seller,
        'cartItems': cart['items'],
        'cartSubTotal': cart['subtotal'],
        'cartTotal': cart['total'],

    }

    return render(request, 'shop/cart.html', context)


def checkout(request, seller_name):
    cart = cookieCart(request, seller_name)

    print(request.COOKIES.get('cart'))

    seller = Seller.objects.get(name=seller_name)

    context = {
        'seller': seller,
        'cartItems': cart['items'],
        'cartSubTotal': cart['subtotal'],
        'cartTotal': cart['total'],
        'order': str(request.COOKIES.get('cart')),
    }

    return render(request, 'shop/checkout.html', context)


def create_order(request, seller_name):
    data = json.loads(request.body)

    print(f"data: {request.body}")

    seller = Seller.objects.get(name=seller_name)

    order_dict = decodeOrder(data['order'], seller)

    print(data['order_information'])

    parent_order = ParentOrder.objects.create(
        first_name=data['order_information']['first_name'],
        last_name=data['order_information']['last_name'],
        street_name=data['order_information']['street_name'],
        house_number=data['order_information']['house_number'],
        postal_code=data['order_information']['postal_code'],
        city=data['order_information']['city'],
        message=request.COOKIES.get('cartMessage'),
    )

    for item_dict in order_dict['items']:
        item_seller = item_dict['object'].seller
        if parent_order.order_set.filter(seller=item_seller):
            order = parent_order.order_set.get(seller=item_seller)
        else:
            order = Order.objects.create(
                parent_order=parent_order,
                seller=item_seller,
                total=item_seller.delivery_price
            )
        order_item = OrderItem.objects.create(
            item=item_dict['object'],
            price=item_dict['price'],
            order=order
        )
        order.subtotal += order_item.price
        order.total += order_item.price
        order.save()

    for order in parent_order.order_set.all():
        parent_order.subtotal += order.subtotal
        parent_order.total += order.total
        parent_order.save()

    return redirect(f"/summary/{seller_name}")


def summary(request, seller_name):
    cart = cookieCart(request, seller_name)

    seller = Seller.objects.get(name=seller_name)

    context = {
        'seller': seller,
        'cartItems': cart['items'],
        'cartSubTotal': cart['subtotal'],
        'cartTotal': cart['total'],
    }

    return render(request, 'shop/summary.html', context)


def cart_total(request, seller_name):
    cart = cookieCart(request, seller_name)

    seller = Seller.objects.get(name=seller_name)

    context = {
        'seller': seller,
        'cartSubTotal': cart['subtotal'],
        'cartTotal': cart['total'],
    }

    print(context)

    return render(request, 'shop/cart_total.html', context)


def cart_preview(request, seller_name):
    cart = cookieCart(request, seller_name)

    seller = Seller.objects.get(name=seller_name)

    context = {
        'seller': seller,
        'cartItems': cart['items'],
        'cartSubTotal': cart['subtotal'],
        'cartTotal': cart['total'],
    }

    return render(request, 'shop/cart_preview.html', context)


def shop_items(request, seller_name):
    search = json.loads(request.COOKIES['search'])
    category_id = search['category']
    sort = search['sort']
    keyword = search['keyword']

    seller = Seller.objects.get(name=seller_name)

    if seller_name != 'encomi':

        if category_id != 0:
            try:
                category = seller.category_set.get(id=category_id)
                items = seller.item_set.filter(categories=category)
            except:
                items = seller.item_set.all()
        else:
            items = seller.item_set.all()

    else:
        if category_id != 0:
            try:
                category = Category.objects.get(id=category_id)
                items = Item.objects.filter(categories=category)
            except:
                items = Item.objects.item_set.all()
        else:
            items = Item.objects.all()

    if sort == 'Best':
        items = items.order_by('id')
    elif sort == 'Ascending':
        items = items.order_by('price')
    elif sort == 'Descending':
        items = items.order_by('-price')

    if not keyword == 'all':
        items = items.filter(title__contains=keyword)

    print(items.order_by('-price'))

    context = {
        'seller': seller,
        'items': items,
    }

    return render(request, 'shop/shop_items.html', context)


def scrape(request):

    scrapeEtsy()

    return redirect(home)


def become_seller(request):

    context = {}

    return render(request, 'shop/become_seller.html', context)


def dashboard(request):

    context = {}

    return render(request, 'shop/dashboard.html', context)


def listings(request):

    context = {}

    return render(request, 'shop/listings_dashboard.html', context)


def categories(request):

    context = {}

    return render(request, 'shop/categories_dashboard.html', context)


def deliveries(request):

    context = {}

    return render(request, 'shop/deliveries_dashboard.html', context)


def settings(request):

    context = {}

    return render(request, 'shop/settings_dashboard.html', context)

def seller_policy(request):

    context = {}

    return render(request, 'shop/seller_policy.html', context)

def privacy_policy(request):

    context = {}

    return render(request, 'shop/privacy_policy.html', context)

def TOU(request):

    context = {}

    return render(request, 'shop/TOU.html', context)

def about(request):

    context = {}

    return render(request, 'shop/about.html', context)