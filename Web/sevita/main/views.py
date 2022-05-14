from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404

from main.models import Product

header = [{'title': "О нас", 'url_name': 'about'},
          {'title': "Каталог", 'url_name': 'catalog'},
          {'title': "Оплата", 'url_name': 'payment'},
          {'title': "Контакты", 'url_name': 'contacts'}
          ]


def index(request):
    products_count = Product.objects.count()
    # Получение последних 8 товаров для отображения на главной странице
    if products_count >= 8:
        products = Product.objects.filter(pk__gte=products_count - 8)
    else:
        products = Product.objects.all()

    context = {
        'title': 'SEVITA exclusive',
        'header': header,
        'products': products,
        'page': 'home'
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


# Отображение страницы с товаром
def show_product(request, prod_id):
    prod = get_object_or_404(Product, pk=prod_id)

    context = {
        'prod': prod,
        'header': header,
        'title': prod.title,
    }

    return render(request, 'main/product.html', context=context)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
