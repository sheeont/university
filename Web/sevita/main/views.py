from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import *
from .models import *
from .telegram import send_contacts

header = [{'title': "О нас", 'url_name': 'home'},
          {'title': "Каталог", 'url_name': 'catalog'},
          {'title': "Оплата", 'url_name': 'payment'},
          {'title': "Контакты", 'url_name': 'contacts'}
          ]


def index(request):
    context = {
        'title': 'SEVITA exclusive',
        'header': header,
        'page': 'home'
    }

    return render(request, 'main/index.html', context=context)


def about(request):
    return HttpResponse('about')


def catalog(request):
    products = Product.objects.all()

    context = {
        'title': 'Каталог',
        'header': header,
        'products': products,
        'page': 'catalog'
    }

    return render(request, 'main/catalog.html', context=context)


def payment(request):
    return HttpResponse('payment')


def contacts(request):
    return HttpResponse('contacts')


# Отображение страницы с товаром
def show_product(request, prod_slug):
    prod = get_object_or_404(Product, slug=prod_slug)
    if request.method == 'POST':
        form = FeedBack(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            message_to_send = f"Товар: {data['product']}\nОбъём флакончика: {CHOICES[int(data['volume'])][1]}\n" \
                              f"E-mail: {data['contacts']}\n"

            if data['description']:
                message_to_send += f"Сообщение от отправителя: {data['description']}"
            try:
                send_contacts(message_to_send)
                return redirect('home')
            except:
                form.add_error(None, "Ошибка отправки формы. Попробуйте позднее.")
    else:
        form = FeedBack()

    context = {
        'prod': prod,
        'header': header,
        'title': prod.title,
        'page': 'product',
        'form': form
    }

    return render(request, 'main/product.html', context=context)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])

            new_user.save()
            return redirect('home')
    else:
        user_form = UserRegistrationForm()

    context = {
        'title': 'Регистрация',
        'user_form': user_form,
    }

    return render(request, 'main/register.html', context=context)
