from django.http import JsonResponse
from django.shortcuts import render
from .services import *


# Create your views here.
def index(request):
    """Отображение главной страницы"""
    dict_obj = {'review_list_start': get_approved_reviews(0, 3),
                'review_list_end': get_approved_reviews_three_in_a_row(30), }
    return render(request, 'index.html', dict_obj)


def feedback(request):
    """Вывод страницы с отзывами"""
    page = 1
    pages = get_count_pages_approved_reviews()
    if not request.GET.get('page') is None:
        page = int(request.GET.get('page'))
    if page > pages:
        page = 1
    dict_obj = {'reviews': get_reviews_to_feedback_list(page),
                'pages': range(1, pages + 1),
                'page': page, }
    return render(request, 'feedback_list.html', dict_obj)


def request_service(request):
    """Обработка отправки заявки на прием из ajax"""
    if request.method == "POST":
        register_a_service_request(request.POST.get('fio'), request.POST.get('phone'),
                                   request.POST.get('info'))
        return JsonResponse({"success": True}, status=200)
    return JsonResponse({"success": False}, status=400)


def post_review(request):
    """Сохранение отзыва"""
    if request.method == "POST":
        save_review(request.POST.get('fio'), request.POST.get('info'))
        return JsonResponse({"success": True}, status=200)
    return JsonResponse({"success": False}, status=400)


def price_list(request):
    """Вывод прайс листа"""
    groups = GroupService.objects.all().order_by('num_order', 'name')
    dict_obj = {'groups': groups}
    return render(request, 'price.html', dict_obj)


def for_clients(request):
    """Вывод страницы 'Для клиентов' """
    from ais.services import get_photos
    dict_obj = {'photos': get_photos(), }
    return render(request, 'for_clients.html', dict_obj)


def prevention(request):
    """Вывод страницы 'профилактика' """
    dict_obj = {}
    return render(request, 'prevention.html', dict_obj)


def contacts(request):
    """Вывод страницы 'Контакты' """
    dict_obj = {}
    return render(request, 'contacts.html', dict_obj)


def about(request):
    """Вывод страницы 'О кабинете' """
    dict_obj = {}
    return render(request, 'about.html', dict_obj)


def discounts(request):
    """Вывод страницы 'Акции' """
    dict_obj = {'discounts': get_active_promotions(), }
    return render(request, 'discounts.html', dict_obj)


def agreement(request):
    """Вывод страницы 'Согласие на обработку перс данных' """
    dict_obj = {}
    return render(request, 'agreement.html', dict_obj)
