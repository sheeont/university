from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView

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
        context['user_form'] = self.register(self.request)
        return context

    def get_queryset(self):
        """
        Функция выводит только те объекты из базы данных, которые отмечены, как видимые и, так как это неполный каталог
        (каталог главной страницы), то устанавливает ограничение на количество выводимых объектов (count).
        """
        count = 8
        return Product.objects.filter(is_visible=True, pk__gte=Product.objects.count() - count + 1)

    def register(self, request):
        if request.method == 'POST':
            user_form = UserRegistrationForm(request.POST)
            if user_form.is_valid():
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data['password'])

                new_user.save()
                return redirect('home')
        else:
            user_form = UserRegistrationForm()
        return user_form


class MainCatalog(ListView):
    model = Product
    template_name = "main/catalog.html"
    context_object_name = 'products'

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


class ShowProduct(DetailView):
    model = Product
    template_name = 'main/product.html'
    slug_url_kwarg = 'prod_slug'
    context_object_name = 'prod'

    def get_context_data(self, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['prod']
        context['header'] = header
        context['page'] = 'product'
        context['form'] = self.get_form(self.request)
        return context

    def get_form(self, request):
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

        return form


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
