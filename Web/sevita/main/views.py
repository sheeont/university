from django.http import HttpResponse
from django.shortcuts import render

header = [{'title': "О нас", 'url_name': 'about'},
          {'title': "Каталог", 'url_name': 'catalog'},
          {'title': "Оплата", 'url_name': 'payment'},
          {'title': "Контакты", 'url_name': 'contacts'}
          ]


def index(request):
    context = {
        'title': 'SEVITA exclusive',
        'header': header,
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
