import json
from .models import *
from datetime import datetime, timedelta


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

        print(item_object.seller, seller)
        if item_object.seller.name == seller or seller == 'encomi':
            subtotal += item_dict['quantity'] * price
            total += item_dict['quantity'] * price

        if item_object.seller not in seller_list:
            total += item_object.seller.delivery_price
            seller_list.append(item_object.seller)

    shipping = total - subtotal

    print(items, subtotal, total)

    return {'items': items, 'subtotal': subtotal, 'total': total, 'shipping': shipping}


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


def deliveryDateCalculator(cart):
    today = datetime.now()

    first_delivery_date = datetime.now() + timedelta(days=1000)
    last_delivery_date = datetime.now()

    for item in cart['items']:
        item_seller = Seller.objects.get(name=item['object'].seller)
        date = today + timedelta(days=item_seller.delivery_days)
        if date < first_delivery_date:
            first_delivery_date = date
        if date > last_delivery_date:
            last_delivery_date = date

    if first_delivery_date != last_delivery_date:
        delivery_date = f"{first_delivery_date.strftime('%A, %d. %b')} - {last_delivery_date.strftime('%A, %d. %b')}"
    else:
        delivery_date = f"{first_delivery_date.strftime('%A, %d. %b')}"

    return delivery_date


def salesStatistics(seller, days):
    today = datetime.today()

    weekday_list = []

    sales_list = []

    for i in range(days):
        sales = 0
        day = today - timedelta(days=i)
        orders = Order.objects.filter(seller=seller)
        for order in orders:
            print(order.parent_order.datetime.day, day.day)
            if order.parent_order.datetime.day == day.day:
                sales += 1
                print(day)

        sales_list.append(sales)

        weekday = day.strftime("%A")
        print(weekday)
        weekday_list.append(weekday)

    weekday_list.reverse()
    sales_list.reverse()

    return {'weekday_list': weekday_list, 'sales_list': sales_list}
