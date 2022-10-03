import json
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import *
from .utils import *
from .scraper import *
from .forms import *
from django.http import HttpResponseRedirect, JsonResponse

from django.contrib.auth import authenticate, login, logout


def base(request):
    # return redirect('become_seller')
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
        'user': request.user,
    }

    home_template = f"shop/{seller}_home.html"

    return render(request, home_template, context)


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


    items = seller.item_set.all()


    context = {
        'seller': seller,
        'item': item,
        'items': items,
        'cartItems': cart['items'],
        'cartTotal': cart['total'],
        'categories': categories,
    }

    return render(request, 'shop/item.html', context)


def cart(request, seller_name):
    cart = cookieCart(request, seller_name)

    seller = Seller.objects.get(name=seller_name)
    categories = seller.category_set.all()

    delivery_date = deliveryDateCalculator(cart)

    context = {
        'seller': seller,
        'cartItems': cart['items'],
        'cartSubTotal': cart['subtotal'],
        'cartTotal': cart['total'],
        'shipping': cart['shipping'],
        'categories': categories,
        'deliveryDate': delivery_date,
    }

    return render(request, 'shop/cart.html', context)


def checkout(request, seller_name):
    cart = cookieCart(request, seller_name)

    print(request.COOKIES.get('cart'))

    seller = Seller.objects.get(name=seller_name)

    delivery_date = deliveryDateCalculator(cart)

    context = {
        'seller': seller,
        'cartItems': cart['items'],
        'cartSubTotal': cart['subtotal'],
        'cartTotal': cart['total'],
        'shipping': cart['shipping'],
        'order': str(request.COOKIES.get('cart')),
        'deliveryDate': delivery_date,
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
        datetime=datetime.now(),
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
            quantity=item_dict['quantity'],
            order=order
        )
        print(item_dict['style_groups'].items())
        for style_group, style in item_dict['style_groups'].items():
            style_group_object = order_item.item.stylegroup_set.get(type=style_group)
            style_object = style_group_object.style_set.get(title=style)
            order_item_style_group = OrderItemStyleGroup.objects.create(
                order_item=order_item,
                style_group=style_group_object,
                selected_style=style_object,
            )
            order_item_style_group.save()

        order.subtotal += order_item.price * order_item.quantity
        order.total += order_item.price * order_item.quantity
        order.save()

    for order in parent_order.order_set.all():
        parent_order.subtotal += order.subtotal
        parent_order.total += order.total
        parent_order.save()

    return redirect(f"/thankyou/{seller_name}")


def thankyou(request, seller_name):
    cart = cookieCart(request, seller_name)

    seller = Seller.objects.get(name=seller_name)

    form = NewsletterEmailForm()

    submitted = False

    if request.method == 'POST':
        form = NewsletterEmailForm(request.POST)
        print(form)
        if form.is_valid():
            print(form)
            try:
                email = NewsletterEmail.objects.create(
                    email=form.cleaned_data['email'],
                    datetime=datetime.now(),
                )
                print(email)
                email.save()
                submitted = True

            except:
                print('issue')
                return redirect(f"/thankyou/{seller_name}")

    delivery_date = deliveryDateCalculator(cart)

    context = {
        'seller': seller,
        'cartItems': cart['items'],
        'cartSubTotal': cart['subtotal'],
        'cartTotal': cart['total'],
        'shipping': cart['shipping'],
        'form': form,
        'submitted': submitted,
        'deliveryDate': delivery_date,
    }

    return render(request, 'shop/thankyou.html', context)


def cart_total(request, seller_name):
    cart = cookieCart(request, seller_name)

    seller = Seller.objects.get(name=seller_name)

    context = {
        'seller': seller,
        'cartSubTotal': cart['subtotal'],
        'cartTotal': cart['total'],
        'shipping': cart['shipping'],
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
        'shipping': cart['shipping'],
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


def scrape(request, seller_name):
    seller = Seller.objects.get(name=seller_name)

    scrapeEtsy(seller)

    return redirect(home)


def become_seller(request):

    form = SellerApplicationForm()

    submitted = False

    if request.method == 'POST':
        form = SellerApplicationForm(request.POST)
        print(form)
        if form.is_valid():
            print(form)
            try:
                seller_application = SellerApplication.objects.create(
                    email=form.cleaned_data['email'],
                    shop_name=form.cleaned_data['shop_name'],
                )
                print(seller_application)
                seller_application.save()
                submitted = True

            except:
                return redirect('/')

    context = {
        'form': form,
        'submitted': submitted,
    }

    return render(request, 'shop/become_seller.html', context)


def dashboard(request, seller_name):
    seller = Seller.objects.get(name=seller_name)

    sales_chart = salesStatistics(seller, 7)

    orders = Order.objects.filter(seller=seller).order_by('-id')

    items = Item.objects.all()[:5]

    revenue = 0

    old_revenue = 0

    day_30_days = timezone.now() - timedelta(30)

    day_60_days = timezone.now() - timedelta(30)

    for order in orders:
        if order.parent_order.datetime >= day_30_days:
            revenue += order.total
        elif order.parent_order.datetime >= day_60_days:
            old_revenue += order.total

    try:
        revenue_change = (revenue - old_revenue) / old_revenue * 100
    except ZeroDivisionError:
        revenue_change = 10000

    context = {
        'seller': seller,
        'weekday_list': sales_chart['weekday_list'],
        'sales_list': sales_chart['sales_list'],
        'orders': orders,
        'items': items,
        'revenue': revenue,
        'revenue_change': revenue_change,
    }

    return render(request, 'shop/home_dashboard.html', context)


def listings(request, seller_name):

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

    print(categories)

    context = {
        'seller': seller,
        'items': items,
        'categories': categories,
    }

    return render(request, 'shop/listings_dashboard.html', context)


def listings_items(request, seller_name):
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


    context = {
        'seller': seller,
        'items': items,
    }

    return render(request, 'shop/listings_dashboard_items.html', context)


def deliveries(request, order_id, seller_name):
    seller = Seller.objects.get(name=seller_name)

    orders = Order.objects.filter(seller=seller).order_by('-id')

    if order_id != 'last':
        selected_order = Order.objects.get(id=order_id)
    else:
        selected_order = Order.objects.filter(seller=seller).last()

    context = {
        'seller': seller,
        'orders': orders,
        'selected_order': selected_order,
    }

    return render(request, 'shop/deliveries_dashboard.html', context)


def deliveries_selected(request, seller_name, order_id):
    seller = Seller.objects.get(name=seller_name)

    selected_order = Order.objects.get(id=order_id)

    context = {
        'selected_order': selected_order,
        'seller': seller,
    }

    return render(request, 'shop/selected_order.html', context)


def update_order_status(request, seller_name, order_id, order_status):
    seller = Seller.objects.get(name=seller_name)

    selected_order = Order.objects.get(id=order_id)
    selected_order.status = order_status
    selected_order.save()

    context = {
        'selected_order': selected_order,
        'seller': seller,
    }

    return render(request, 'shop/selected_order_status.html', context)


def settings(request, seller_name):
    seller = Seller.objects.get(name=seller_name)

    seller_policies = seller.policies
    if not seller_policies:
        seller_policies = SellerPolicies.objects.create()
        seller.policies = seller_policies
        seller.save()
    policies_form = PoliciesForm(instance=seller_policies)

    if request.method == 'POST':
        form = PoliciesForm(request.POST, instance=seller_policies)
        print(request.POST['shipping_general_information'])
        print(seller_policies.shipping_general_information)
        if form.is_valid():
            form.save()
            print(seller_policies.shipping_general_information)

        return redirect(f"/dashboard/settings/{seller}")

    context = {
        'seller': seller,
        'policies_form': policies_form,
    }

    return render(request, 'shop/settings_dashboard.html', context)


def update_settings_content(request, seller_name, content):
    seller = Seller.objects.get(name=seller_name)

    template = f"shop/settings_dashboard_{content}.html"

    seller_policies = seller.policies
    if not seller_policies:
        seller_policies = SellerPolicies.objects.create()
        seller.policies = seller_policies
        seller.save()
    policies_form = PoliciesForm(instance=seller_policies)

    context = {
        'seller': seller,
        'policies_form': policies_form,
    }

    return render(request, template, context)


def seller_policy(request, seller_name):
    seller = Seller.objects.get(name=seller_name)

    context = {
        'seller': seller,
    }

    return render(request, 'shop/seller_policy.html', context)

def privacy_policy(request, seller_name):
    seller = Seller.objects.get(name=seller_name)

    context = {
        'seller': seller,
    }

    return render(request, 'shop/privacy_policy.html', context)

def TOU(request, seller_name):
    seller = Seller.objects.get(name=seller_name)

    context = {
        'seller': seller,
    }

    return render(request, 'shop/TOU.html', context)

def about(request, seller_name):
    seller = Seller.objects.get(name=seller_name)

    context = {
        'seller': seller,
    }

    return render(request, 'shop/about.html', context)


def register_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                try:
                    new_user = authenticate(email=form.cleaned_data['email'],
                                            password=form.cleaned_data['password'],
                                            )
                    login(request, new_user)

                    return redirect('/')

                except:
                    return redirect('/register/')

        context = {'form': form}

        return render(request, 'shop/register.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = AuthenticateUserForm()
        if request.method == 'POST':
            form = AuthenticateUserForm(request.POST)
            if form.is_valid():
                try:
                    new_user = authenticate(email=form.cleaned_data['email'],
                                            password=form.cleaned_data['password'],
                                            )
                    login(request, new_user)

                    return redirect('/')

                except:
                    return redirect('/login/')

        context = {'form': form}

        return render(request, 'shop/login.html', context)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def help(request, seller_name):
    seller = Seller.objects.get(name=seller_name)

    faqs = FAQ.objects.filter(type='buyer')

    form = HelpMessageForm()

    submitted = False

    if request.method == 'POST':
        form = HelpMessageForm(request.POST)
        print(form)
        if form.is_valid():
            print(form)
            try:
                message = HelpMessage.objects.create(
                    email=form.cleaned_data['email'],
                    message=form.cleaned_data['message'],
                )
                print(message)
                message.save()
                submitted = True

            except:
                print('issue')
                return redirect('/')

    context = {
        'seller': seller,
        'faqs': faqs,
        'form': form,
        'submitted': submitted
    }

    return render(request, 'shop/help.html', context)


def help_faqs(request, seller_name, type):
    seller = Seller.objects.get(name=seller_name)

    faqs = FAQ.objects.filter(type=type)

    context = {
        'seller': seller,
        'faqs': faqs,
    }

    return render(request, 'shop/help_faqs.html', context)

