import json
from django.shortcuts import render
from .models import Item, Category
from .utils import cookieCart

# Create your views here.


def home(request):

    cart = cookieCart(request)

    items = Item.objects.all()

    context = {
        'items': items,
        'cartItems': cart['items'],
        'cartTotal': cart['total'],
    }

    return render(request, 'shop/home.html', context)


def shop(request):
    search = json.loads(request.COOKIES['search'])
    category_id = search['category']
    sort = search['sort']
    keyword = search['keyword']

    cart = cookieCart(request)

    if category_id != 0:
        category = Category.objects.get(id=category_id)
        items = Item.objects.filter(categories=category)
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

    categories = Category.objects.all()

    """for item in items:
        for style_group in item.style_groups.all():
            print(style_group.type)
            for style in style_group.styles.all():
                print(style.title)
    """

    context = {
        'items': items,
        'categories': categories,
        'cartItems': cart['items'],
        'cartTotal': cart['total'],
    }

    return render(request, 'shop/shop.html', context)


def item(request, id):

    cart = cookieCart(request)

    item = Item.objects.get(id=id)

    context = {
        'item': item,
        'cartItems': cart['items'],
        'cartTotal': cart['total'],
    }

    return render(request, 'shop/item.html', context)


def cart(request):

    cart_items = Item.objects.filter()  # filter for in cart

    cookieCart(request)

    context = {
        'cart_items': cart_items,
    }

    return render(request, 'shop/cart.html', context)


def cart_preview(request):
    cart = cookieCart(request)

    context = {
        'cartItems': cart['items'],
        'cartTotal': cart['total'],
    }

    return render(request, 'shop/cart_preview.html', context)


def shop_items(request):
    search = json.loads(request.COOKIES['search'])
    category_id = search['category']
    sort = search['sort']
    keyword = search['keyword']

    if category_id != 0:
        category = Category.objects.get(id=category_id)
        items = Item.objects.filter(categories=category)
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
        'items': items,
    }

    return render(request, 'shop/shop_items.html', context)