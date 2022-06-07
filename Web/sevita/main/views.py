from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

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
        c_def = self.get_user_context(title="SEVITA exclusive", page="home", sync_data=sync_data(self.request))

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        """
        Функция выводит только те объекты из базы данных, которые отмечены, как видимые и, так как это неполный каталог
        (каталог главной страницы), то устанавливает ограничение на количество выводимых объектов (count).
        """
        count = 8
        return Product.objects.filter(is_visible=True, pk__gte=Product.objects.count() - count + 1)


class MainCatalog(DataMixin, ListView):
    paginate_by = 12
    model = Product
    template_name = "main/catalog.html"
    context_object_name = 'products'

    def get_context_data(self, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Каталог", page="catalog", sync_data=sync_data(self.request))

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


class RegisterUser(DataMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация", page="register", form=self.reg(self.request))

        return dict(list(context.items()) + list(c_def.items()))

    def reg(self, request):
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


# Функции для AJAX
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def add_to_favorites(request):
    if request.method == 'POST':
        if not request.session.get('favorites'):
            request.session['favorites'] = list()
        else:
            request.session['favorites'] = list(request.session['favorites'])

        # Проверяем, находится ли товар в списке словарей избранных товаров
        item_exists = next((item for item in request.session['favorites'] if item['type'] == request.POST.get('type')
                            and item['id'] == request.POST.get('id')), False)

        # Получаем данные из POST-запроса
        add_data = {
            'type': request.POST.get('type'),
            'id': request.POST.get('id'),
        }

        if not item_exists:
            request.session['favorites'].append(add_data)
            request.session.modified = True

    # Для AJAX запросов
    if is_ajax(request):
        data = {
            'type': request.POST.get('type'),
            'id': request.POST.get('id'),
        }
        request.session.modified = True

        # Добавление избранного товара в базу данных
        if request.user.is_authenticated:
            send_to_db(request=request, data=data)

        return JsonResponse(data)

    return redirect(request.POST.get('url_from'))


def send_to_db(request, data):
    if data['type'] == "product":
        prod = Product.objects.get(id=data['id'])
        user = auth.get_user(request)

        # Пытаемся получить избранное из таблицы, или создать новую
        favorite, created = Favorites.objects.get_or_create(user=user, obj_id=prod.pk)

        # Если новый товар не добавлен в избранное, значит, он там уже есть, а значит,
        # клик по этому товару будем считать запросом на удаление его из избранного
        if not created:
            favorite.delete()


def remove_from_favorites(request):
    if request.method == 'POST':
        # Удаление товара из избранных
        for item in request.session['favorites']:
            if item['id'] == request.POST.get('id') and item['type'] == request.POST.get('type'):
                item.clear()

        # После удаления товара, убираем из списка пустой словарь
        while {} in request.session['favorites']:
            request.session['favorites'].remove({})

        # Удаляем список со словарями избранных товаров, если этот список пуст
        if not request.session['favorites']:
            del request.session['favorites']

        request.session.modified = True

    # Для AJAX запросов
    if is_ajax(request):
        data = {
            'type': request.POST.get('type'),
            'id': request.POST.get('id'),
        }
        request.session.modified = True

        # Удаление избранного товара из базы данных
        if request.user.is_authenticated:
            send_to_db(request=request, data=data)

        return JsonResponse(data)

    return redirect(request.POST.get('url_from'))


# Синхронизация данных сессии и модели для корректного отображения кнопок 'Избранное'
def sync_data(request):
    model_type = "product"
    # Проверяем, авторизирован ли пользователь
    if request.user.is_authenticated:
        # Инициализируем список словарей, в котором лежат избранные сессии
        if not request.session.get('favorites'):
            request.session['favorites'] = list()
        else:
            request.session['favorites'] = list(request.session['favorites'])

        # Если избранных в сессии нет, но в БД есть, то:
        if not request.session.get('favorites') and Favorites.objects.count():
            # Добавляем в сессию те объекты, которые есть в БД
            for prod in Product.objects.all():
                # Получаем все избранные текущего пользователя
                favorites_set = prod.favorites_set.filter(user=request.user)
                # Добавляем избранные товары в сессию
                for favorite in favorites_set:
                    request.session['favorites'].append({"type": model_type, "id": str(favorite.obj_id)})

        # Если избранные есть в сессии и в БД, но они не совпадают
        elif request.session.get('favorites') and Favorites.objects.count():
            # Инициализируем список id избранных товаров
            favorites_ids = []

            # Добавляем в сессию те объекты, которые есть в БД, но их нет в самой сессии
            for prod in Product.objects.all():
                # Получаем избранные товары пользователя по очереди
                favorites_set = prod.favorites_set.filter(user=request.user)

                # Если избранных нет, переходим к следующей итерации
                if favorites_set:
                    # Добавляем id текущего избранного товара в список
                    favorites_ids.append(str(favorites_set[0].obj_id))

                    # Получаем id всех товаров, которые есть в сессии
                    all_ids = [item['id'] for item in request.session['favorites']]

                    # Проверяем, существует ли уже такая запись в сессии, если нет, добавляем её.
                    if str(favorites_set[0].obj_id) not in all_ids:
                        request.session['favorites'].append({"type": model_type, "id": favorites_set[0].obj_id})
                        all_ids.append(favorites_set[0].obj_id)

            # По полученному списку id избранных в БД, удаляем из сессии те объекты, которых в этом списке нет
            for item in request.session['favorites']:
                if str(item['id']) not in favorites_ids:
                    item.clear()

            # После удаления товара, убираем из списка пустой словарь
            while {} in request.session['favorites']:
                request.session['favorites'].remove({})


def favorites_api(request):
    return JsonResponse(request.session.get('favorites'), safe=False)
