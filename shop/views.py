from django.shortcuts import render
from .models import Item

# Create your views here.


def home(request):

    items = Item.objects.all()

    context = {
        'items': items,
    }

    return render(request, 'shop/home.html', context)


def shop(request):

    items = Item.objects.all()

    context = {
        'items': items,
    }

    return render(request, 'shop/shop.html', context)


def item(request, id):

    item = Item.objects.get(id=id)

    context = {
        'item': item,
    }

    return render(request, 'shop/item.html', context)


def cart(request):

    cart_items = Item.objects.filter()  # filter for in cart

    context = {
        'cart_items': cart_items,
    }

    return render(request, 'shop/cart.html', context)
