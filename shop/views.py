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
