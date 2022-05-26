from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView

from .forms import *
from .models import *
from .telegram import send_contacts

header = [{'title': "О нас", 'url_name': 'home'},
          {'title': "Каталог", 'url_name': 'catalog'},
          {'title': "Оплата", 'url_name': 'payment'},
          {'title': "Контакты", 'url_name': 'contacts'}
          ]


class MainHome(ListView):
    model = Product
    template_name = "main/index.html"
    context_object_name = 'products'
    extra_context = {'title': 'SEVITA exclusive'}

    def get_context_data(self, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = header
        context['page'] = 'home'
        return context

    """
    Функция выводит только те объекты из базы данных, которые отмечены, как видимые и, так как это неполный каталог
    (каталог главной страницы), то устанавливает ограничение на количество выводимых объектов (count).
    """

    def get_queryset(self):
        count = 8
        return Product.objects.filter(is_visible=True, pk__gte=Product.objects.count() - count + 1)


class MainCatalog(ListView):
    model = Product
    template_name = "main/catalog.html"
    context_object_name = 'products'

    # extra_context = {'title': 'Каталог'}

    def get_context_data(self, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Каталог'
        context['header'] = header
        context['page'] = 'catalog'
        return context

    def get_queryset(self):
        return Product.objects.filter(is_visible=True)


def payment(request):
    return HttpResponse('payment')


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
