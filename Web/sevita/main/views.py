from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from main.models import Product

header = [{'title': "О нас", 'url_name': 'about'},
          {'title': "Каталог", 'url_name': 'catalog'},
          {'title': "Оплата", 'url_name': 'payment'},
          {'title': "Контакты", 'url_name': 'contacts'}
          ]


def index(request):
    products = Product.objects.all()
    context = {
        'title': 'SEVITA exclusive',
        'header': header,
        'products': products
    }

    return render(request, 'main/index.html', context=context)


def about(request):
    return HttpResponse('about')


def catalog(request):
    return HttpResponse('catalog')


def payment(request):
    return HttpResponse('payment')


def contacts(request):
    return HttpResponse('contacts')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
