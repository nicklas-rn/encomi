import json
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

    """for item in items:
        for style_group in item.style_groups.all():
            print(style_group.type)
            for style in style_group.styles.all():
                print(style.title)
    """

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

    cookieCart(request)

    context = {
        'cart_items': cart_items,
    }

    return render(request, 'shop/cart.html', context)



def cookieCart(request):
    # Create empty cart for now for non-logged in user
    try:
        cart = json.loads(request.COOKIES['cart'])

    except:
        cart = {}
        print('CART:', cart)

    items = []

    print(cart)

    total = 0

    for k in cart:
        item_object = Item.objects.get(id=cart[k]['itemId'])
        price = item_object.price
        for l in cart[k]['style_groups']:
            if item_object.stylegroup_set.get(type=l).style_set.get(title=cart[k]['style_groups'][l]).price:
                price = item_object.stylegroup_set.get(type=l).style_set.get(title=cart[k]['style_groups'][l]).price

        print(price)

        item_dict = {
            'object': item_object,
            'style_groups': cart[k]['style_groups'],
            'quantity': cart[k]['quantity'],
            'price': price,
        }
        items.append(item_dict)

        total += item_dict['quantity'] * price


    print(items, total)

    return {'items': items}
