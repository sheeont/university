from django.shortcuts import redirect

from .forms import UserRegistrationForm

header = [{'title': "О нас", 'url_name': 'home'},
          {'title': "Каталог", 'url_name': 'catalog'},
          {'title': "Оплата", 'url_name': 'payment'},
          {'title': "Контакты", 'url_name': 'contacts'}
          ]


def reg(request):
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


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['header'] = header
        context['user_form'] = reg(self.request)

        return context
