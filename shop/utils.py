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

    print(cart)

    total = 0

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
            total += item_dict['quantity'] * price

    print(items, total)

    return {'items': items, 'total': total}