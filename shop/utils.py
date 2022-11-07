import json, string, random
from .models import *
from datetime import datetime, timedelta
from django.db.models import Q

fill_words = ['the', 'or', 'and', 'plain', 'set']
type_words = ['necklace', 'bracelet', 'ring', 'rings', 'earring', 'earrings', 'ear climbers']


def sortItems(items):
    items = items.extra(order_by=['?'])
    return items


def generateId(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def getRecommendedItems(request, seller):
    title = []

    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    for k in cart:
        item_object = Item.objects.get(id=cart[k]['itemId'])
        for word in item_object.title.split():
            if word.lower() not in fill_words:
                title.append(word)
                print(word)

    if cart:
        if seller != 'encomi':
            query = Q()
            for word in title:
                query = query | Q(title__contains=word, status='In stock')

            items = seller.item_set.filter(query)

        else:
            query = Q()
            for word in title:
                query = query | Q(title_contains=word, status='In stock')

            items = Item.objects.filter(query)

    else:
        if seller != 'encomi':
            items = seller.item_set.filter(status='In stock')
        else:
            items = Item.objects.filter(status='In stock')

    return items


def getFocusedItems(seller):
    if seller != 'encomi':
        items = seller.item_set.filter(status='In stock').order_by('sold_counter')
    else:
        items = Item.objects.filter(status='In stock').order_by('sold_counter')
    return items


def getSimilarItems(seller, item):
    title = []

    for word in item.title.split():
        if word.lower() not in fill_words:
            title.append(word)
            print(word)

    if seller != 'encomi':
        query = Q()
        for word in title:
            query = query | Q(title__contains=word, status='In stock')

        items = seller.item_set.filter(query)

    else:
        query = Q()
        for word in title:
            query = query | Q(title_contains=word, status='In stock')

        items = Item.objects.filter(query)

    return items


def getComplementaryItems(seller, item):
    title = []

    for word in item.title.split():
        if word.lower() not in fill_words:
            title.append(word)
            print(word)

    if seller != 'encomi':
        include_query = Q()
        for word in title:
            if word.lower() not in type_words:
                include_query = include_query | Q(title__contains=word, status='In stock')

        exclude_query = Q()
        for word in title:
            if word.lower() in type_words:
                exclude_query = exclude_query | Q(title__contains=word)
        items = seller.item_set.filter(include_query).exclude(exclude_query)

    else:
        query = Q()
        for word in title:
            query = query | Q(title_contains=word, status='In stock')

        items = Item.objects.filter(query)

    return items


def getRandomNumber(min, max):
    return random.randint(min, max)


def cookieCart(request, seller):
    try:
        cart = json.loads(request.COOKIES['cart'])

    except:
        cart = {}
        print('CART:', cart)

    items = []

    subtotal = 0
    total = 0

    seller_list = []

    print(cart)

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


def deliveryDateCalculator(items):
    today = datetime.now()

    first_delivery_date = datetime.now() + timedelta(days=1000)
    last_delivery_date = datetime.now()

    for item in items:
        item_seller = Seller.objects.get(name=item['object'].seller)
        min_date = today + timedelta(days=item_seller.delivery_days_min)
        max_date = today + timedelta(days=item_seller.delivery_days_max)
        if min_date < first_delivery_date:
            first_delivery_date = min_date
        if max_date > last_delivery_date:
            last_delivery_date = max_date

    if first_delivery_date != last_delivery_date:
        delivery_date = f"{first_delivery_date.strftime('%a %d. %b')} - {last_delivery_date.strftime('%a %d. %b')}"
    else:
        delivery_date = f"{first_delivery_date.strftime('%a %d. %b')}"

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
            if order.parent_order.datetime.date() == day.date():
                sales += 1

        sales_list.append(sales)

        weekday = day.strftime("%A")
        print(weekday)
        weekday_list.append(weekday)

    weekday_list.reverse()
    sales_list.reverse()

    return {'weekday_list': weekday_list, 'sales_list': sales_list}
