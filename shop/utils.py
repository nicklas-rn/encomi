import json
from .models import Item


def cookieCart(request, seller):
    # Create empty cart for now for non-logged in user
    try:
        cart = json.loads(request.COOKIES['cart'])

    except:
        cart = {}
        print('CART:', cart)

    items = []

    subtotal = 0
    total = 0

    seller_list = []

    for k in cart:
        item_object = Item.objects.get(id=cart[k]['itemId'])
        price = item_object.price
        for l in cart[k]['style_groups']:
            print(item_object.stylegroup_set.all())
            if item_object.stylegroup_set.get(type=l).style_set.get(title=cart[k]['style_groups'][l]).price:
                price = item_object.stylegroup_set.get(type=l).style_set.get(title=cart[k]['style_groups'][l]).price

        print(price)

        item_dict = {
            'cart_id': k,
            'object': item_object,
            'style_groups': cart[k]['style_groups'],
            'quantity': cart[k]['quantity'],
            'price': price,
        }
        items.append(item_dict)

        if item_object.seller == seller or seller == 'encomi':
            subtotal += item_dict['quantity'] * price
            total += item_dict['quantity'] * price

        if item_object.seller not in seller_list:
            total += item_object.seller.delivery_price
            seller_list.append(item_object.seller)

    print(items, subtotal, total)

    return {'items': items, 'subtotal': subtotal, 'total': total}


def decodeOrder(data, seller):
    items = []

    total = 0

    for k in data:
        item_object = Item.objects.get(id=data[k]['itemId'])
        price = item_object.price
        for l in data[k]['style_groups']:
            print(item_object.stylegroup_set.all())
            if item_object.stylegroup_set.get(type=l).style_set.get(title=data[k]['style_groups'][l]).price:
                price = item_object.stylegroup_set.get(type=l).style_set.get(title=data[k]['style_groups'][l]).price

        print(price)

        item_dict = {
            'cart_id': k,
            'object': item_object,
            'style_groups': data[k]['style_groups'],
            'quantity': data[k]['quantity'],
            'price': price,
        }
        items.append(item_dict)

        if item_object.seller == seller or seller == 'encomi':
            total += item_dict['quantity'] * price

    print(items, total)

    return {'items': items, 'total': total}
