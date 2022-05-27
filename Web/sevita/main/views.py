from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import ListView, DetailView

from .forms import *
from .models import *
from .utils import *
from .telegram import send_contacts


class MainHome(DataMixin, ListView):
    model = Product
    template_name = "main/index.html"
    context_object_name = 'products'

    def get_context_data(self, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="SEVITA exclusive", page="home")

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        """
        Функция выводит только те объекты из базы данных, которые отмечены, как видимые и, так как это неполный каталог
        (каталог главной страницы), то устанавливает ограничение на количество выводимых объектов (count).
        """
        count = 8
        return Product.objects.filter(is_visible=True, pk__gte=Product.objects.count() - count + 1)


class MainCatalog(DataMixin, ListView):
    paginate_by = 20
    model = Product
    template_name = "main/catalog.html"
    context_object_name = 'products'

    def get_context_data(self, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Каталог", page="catalog")

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Product.objects.filter(is_visible=True)


def payment(request):
    return HttpResponse('payment')


class ShowProduct(DataMixin, DetailView):
    model = Product
    template_name = 'main/product.html'
    slug_url_kwarg = 'prod_slug'
    context_object_name = 'prod'

    def get_context_data(self, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['prod'], page="product", form=self.get_form(self.request))

        return dict(list(context.items()) + list(c_def.items()))

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
