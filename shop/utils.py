import json, string, random, requests
from .models import *
from datetime import datetime, timedelta
from django.db.models import Q

fill_words = ['the', 'or', 'and', 'plain', 'set']
type_words = ['necklace', 'bracelet', 'ring', 'rings', 'earring', 'earrings', 'ear climbers']


# Deprecated
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

            items = seller.item_set.filter(query).extra(order_by=['?'])[:20]

        else:
            query = Q()
            for word in title:
                query = query | Q(title_contains=word, status='In stock')

            items = Item.objects.filter(query).extra(order_by=['?'])[:20]

    else:
        if seller != 'encomi':
            items = seller.item_set.filter(status='In stock').extra(order_by=['?'])[:20]
        else:
            items = Item.objects.filter(status='In stock').extra(order_by=['?'])[:20]

    return items


def getFocusedItems(seller):
    if seller != 'encomi':
        items = seller.item_set.filter(status='In stock').order_by('sold_counter').extra(order_by=['?'])[:20]
    else:
        items = Item.objects.filter(status='In stock').order_by('sold_counter').extra(order_by=['?'])[:20]
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

        items = seller.item_set.filter(query).extra(order_by=['?'])[:20]

    else:
        query = Q()
        for word in title:
            query = query | Q(title_contains=word, status='In stock')

        items = Item.objects.filter(query).extra(order_by=['?'])[:20]

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
        items = seller.item_set.filter(include_query).exclude(exclude_query).extra(order_by=['?'])[:20]

    else:
        query = Q()
        for word in title:
            query = query | Q(title_contains=word, status='In stock')

        items = Item.objects.filter(query).extra(order_by=['?'])[:20]

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

    total_fees = total * 0.039

    print(items, subtotal, total)

    return {'items': items, 'subtotal': subtotal, 'total': total, 'totalFees': total_fees, 'shipping': shipping}


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


def getPayPalAccessToken():
    data = {
        'grant_type': 'client_credentials',
    }

    response = requests.post('https://api-m.sandbox.paypal.com/v1/oauth2/token', data=data,
                             auth=(
                                 'ATZy7_w2X0Ec7vhNGRMVvMdFsC5lljVyJ53HKH4Yfi4VdHjdHvUN7ge5q4ZzCaZTgakPs6WcdPfC482w',
                                 'ENvpbwL9xW_Rss8whsLy5AGvO2nxfRhPI7itaONkX2t2XzHbJHN248bud3aY_skc2T0jYfwhEPDSBhKa'
                             )
                             )

    access_token = response.json()['access_token']

    return access_token


def getPayPalActionURL(seller):
    headers = {
        # Already added when you pass json= but not when you pass data=
        # 'Content-Type': 'application/json',
        'Authorization': f'Bearer {getPayPalAccessToken()}',
        'PayPal-Partner-Attribution-Id': 'encomi_SP_PPCP'
    }

    json_data = {
        'tracking_id': f'{seller.pp_tracking_id}',
        'operations': [
            {
                'operation': 'API_INTEGRATION',
                'api_integration_preference': {
                    'rest_api_integration': {
                        'integration_method': 'PAYPAL',
                        'integration_type': 'THIRD_PARTY',
                        'third_party_details': {
                            'features': [
                                'PAYMENT',
                                'REFUND',
                                'ACCESS_MERCHANT_INFORMATION',
                            ],
                        },
                    },
                },
            },
        ],
        'partner_config_override': {
            'return_url': f'https://encomi.co/dashboard/payments/{seller}'
        },

        'products': [
            'EXPRESS_CHECKOUT',
        ],
        'legal_consents': [
            {
                'type': 'SHARE_DATA_CONSENT',
                'granted': True,
            },
        ],
    }

    response = requests.post('https://api-m.sandbox.paypal.com/v2/customer/partner-referrals', headers=headers,
                             json=json_data)

    action_url = response.json()['links'][1]['href']
    print(action_url)

    return action_url


def getSellerPayPalStatus(seller):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {getPayPalAccessToken()}',
        'PayPal-Partner-Attribution-Id': 'encomi_SP_PPCP'
    }

    try:
        seller_merchant_id = requests.get(
            f'https://api-m.sandbox.paypal.com/v1/customer/partners/KDVNVWPCAS786/merchant-integrations?tracking_id={seller.pp_tracking_id}',
            headers=headers
        ).json()['merchant_id']
        print('seller merchant id:', seller_merchant_id)

    except:
        return False

    seller_data = requests.get(
        f'https://api-m.sandbox.paypal.com/v1/customer/partners/KDVNVWPCAS786/merchant-integrations/{seller_merchant_id}',
        headers=headers).json()

    print('response: ', seller_data)

    if not seller.pp_email and seller_data['primary_email_confirmed']:
        seller.pp_email = seller_data['primary_email']
        seller.save()

    return seller_data['primary_email_confirmed']