from django.shortcuts import render

header = ["О нас", "Каталог", "Оплата", "Контакты"]


def index(request):
    return render(request, 'main/index.html', {'title': 'SEVITA exclusive', 'header': header})
