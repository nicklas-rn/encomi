import json
from django.shortcuts import render
from .models import Item
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

    cart = cookieCart(request)

    items = Item.objects.all()

    """for item in items:
        for style_group in item.style_groups.all():
            print(style_group.type)
            for style in style_group.styles.all():
                print(style.title)
    """

    context = {
        'items': items,
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



