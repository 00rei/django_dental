import datetime

from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlencode

from .services import *


def admin_client(request):
    """Вывод информации о клиенте"""
    if is_logged(request) is False:
        return redirect('/')
    if request.GET.get('client_id') is None:
        return redirect('clients')
    if get_client(request.GET.get('client_id')):
        dict_obj = {'new_review_count': get_un_viewed_reviews_count(False),
                    'reg_request_count': get_service_requests(False).count(),
                    'client': get_client(request.GET.get('client_id')),
                    'receptions': get_client_receptions(request.GET.get('client_id')), }
        return render(request, 'admin-client.html', dict_obj)
    else:
        return redirect('clients')


def admin_client_edit(request):
    """Сохранение информации о клиенте"""
    if is_logged(request) is False:
        return redirect('/')
    dict_obj = {'new_review_count': get_un_viewed_reviews_count(False),
                'reg_request_count': get_service_requests(False).count(),
                }
    if request.GET.get('new'):
        return render(request, 'admin-client-edit.html', dict_obj)

    elif request.GET.get('edit'):
        dict_obj = {'new_review_count': get_un_viewed_reviews_count(False),
                    'reg_request_count': get_service_requests(False).count(),
                    'client': get_client(request.GET.get('client_id'))}
        return render(request, 'admin-client-edit.html', dict_obj)

    elif request.GET.get('save'):
        new_id = save_client(client_id=request.GET.get('client_id'), address=request.GET.get('address'),
                             birth_day=request.GET.get('birth_day'), work_place=request.GET.get('work_place'),
                             phone=request.GET.get('phone'), fio=request.GET.get('fio'))

        return redirect('{}?{}'.format(reverse('client'), urlencode({'client_id': new_id})))
    return render(request, 'admin-client-edit.html', dict_obj)

#
# def post(request):
#     dict_obj = {'post': request.POST, }
#     return render(request, 'post.html', dict_obj)
#

def admin_client_reception(request):
    """Прием клиента"""
    if is_logged(request) is False:
        return redirect('/')
    if request.POST.get('save'):
        save_reception(request.POST.get('client_id'), request.POST.getlist('service_id[]'),
                       request.POST.getlist('price[]'), request.POST.get('note'), 1)
        return redirect('{}?{}'.format(reverse('client'), urlencode({'client_id': request.POST.get('client_id')})))
    if request.GET.get('client_id') is None:
        redirect('clients')
    dict_obj = {'new_review_count': get_un_viewed_reviews_count(False),
                'reg_request_count': get_service_requests(False).count(),
                'client': get_client(request.GET.get('client_id')),
                'services': get_services(), }
    return render(request, 'admin-client-reception.html', dict_obj)


def admin_reception_delete(request):
    """Удаление информации о приеме"""
    if is_logged(request) is False:
        return redirect('/')
    if request.GET.get('reception_id'):
        reception_delete(request.GET.get('reception_id'))
    return redirect('{}?{}'.format(reverse('client'), urlencode({'client_id': request.GET.get('client_id')})))


def admin_clients(request):
    """Вывод списка клиентов"""
    if is_logged(request) is False:
        return redirect('/')
    dict_obj = {'new_review_count': get_un_viewed_reviews_count(False),
                'reg_request_count': get_service_requests(False).count(),
                'clients': get_clients(), }
    return render(request, 'admin-clients.html', dict_obj)

#
# def admin_contacts(request):
#     if is_logged(request) is False:
#         return redirect('/')
#     dict_obj = {}
#     return render(request, 'admin-contacts.html', dict_obj)


def admin_discount(request):
    """Вывод страницы со скидками"""
    if is_logged(request) is False:
        return redirect('/')
    dict_obj = {'new_review_count': get_un_viewed_reviews_count(False),
                'reg_request_count': get_service_requests(False).count(),
                'active_promotions': get_active_promotions(),
                'planned_promotions': get_planned_promotions(), }
    return render(request, 'admin-discount.html', dict_obj)


def admin_discount_create(request):
    """Сохранение новой скидки"""
    if is_logged(request) is False:
        return redirect('/')
    create_promotions(request.POST['date_start'], request.POST['date_end'], request.POST['text'],
                      request.session['user_id'])
    return redirect('discount-moderation')


def admin_discount_delete(request):
    """Удаление информации о скидке"""
    if is_logged(request) is False:
        return redirect('/')
    delete_promotions(request.GET['pr_id'])
    return redirect('discount-moderation')


def admin_feedback(request):
    """Вывод страницы с отзывами"""
    if is_logged(request) is False:
        return redirect('/')
    dict_obj = {'new_review_count': get_un_viewed_reviews_count(True),
                'reg_request_count': get_service_requests(False).count(),
                'reviews_no_decision': get_unapproved_reviews(),
                'reviews_approved': get_approved_reviews(),
                'reviews_rejected': get_rejected_reviews(), }
    return render(request, 'admin-feedback.html', dict_obj)


def admin_review_approve(request):
    """Одобрить отзыв"""
    if is_logged(request) is False:
        return redirect('/')
    process_review(request.GET['review_id'], request.session['user_id'], True)
    return redirect('feedback-moderation')


def admin_review_reject(request):
    """Отклонить отзыв"""
    if is_logged(request) is False:
        return redirect('/')
    process_review(request.GET['review_id'], request.session['user_id'], False)
    return redirect('feedback-moderation')


def admin_review_delete(request):
    """Удалить отзыв"""
    if is_logged(request) is False:
        return redirect('/')
    delete_review(request.GET['review_id'])
    return redirect('feedback-moderation')


def admin_photo(request):
    """Работа с фотографиями работ до/после"""
    if is_logged(request) is False:
        return redirect('/')
    if request.method == 'POST' and request.FILES:
        save_photo(request.FILES['photo_before'], request.FILES['photo_after'], request.POST['desc'])
        return redirect('photo')
    dict_obj = {'new_review_count': get_un_viewed_reviews_count(False),
                'reg_request_count': get_service_requests(False).count(),
                'photos': get_photos(), }
    return render(request, 'admin-photo.html', dict_obj)


def admin_photo_delete(request):
    """Удалить запись с фотографиями"""
    if is_logged(request) is False:
        return redirect('/')
    if request.GET.get('photo_id'):
        photo_delete(request.GET.get('photo_id'))
    return redirect('photo')


def admin_price(request):
    """Прайс-лист"""
    if is_logged(request) is False:
        return redirect('/')
    dict_obj = {'new_review_count': get_un_viewed_reviews_count(False),
                'reg_request_count': get_service_requests(False).count(),
                'groups': get_groups_of_service(), }
    return render(request, 'admin-price.html', dict_obj)


def admin_service_delete(request):
    """Удалить услугу"""
    if is_logged(request) is False:
        return redirect('/')
    delete_service(request.GET['service_id'])
    return redirect('price-moderation')


def admin_group_of_service_delete(request):
    """Удалить группу услуг"""
    if is_logged(request) is False:
        return redirect('/')
    delete_group_of_service(request.GET['group_id'])
    return redirect('price-moderation')


def admin_group_of_service_move(request):
    """Переместить группу услуг"""
    if is_logged(request) is False:
        return redirect('/')
    group_move_to(request.GET.get('group_id'), request.GET.get('move_to'))
    return redirect('price-moderation')


def admin_price_edit(request):
    """Изменить информацию об услуге"""
    if is_logged(request) is False:
        return redirect('/')
    if request.GET.get('new'):
        dict_obj = {'new_review_count': get_un_viewed_reviews_count(False),
                    'reg_request_count': get_service_requests(False).count(),
                    'group_id': request.GET['group_id']}
        return render(request, 'admin-price-edit.html', dict_obj)
    elif request.GET.get('save'):
        if request.GET.get('service_id'):
            save_service(request.GET['service_id'], group_id=request.GET['group_id'], name=request.GET['name'],
                         price=request.GET['price'])
            return redirect('price-moderation')
        else:
            save_service(None, group_id=request.GET['group_id'], name=request.GET['name'], price=request.GET['price'])
            return redirect('price-moderation')

    dict_obj = {'new_review_count': get_un_viewed_reviews_count(False),
                'reg_request_count': get_service_requests(False).count(),
                'service': get_service(request.GET['service_id'])}
    return render(request, 'admin-price-edit.html', dict_obj)


def admin_group_of_price_edit(request):
    """Изменить информацию о группе услуг"""
    if is_logged(request) is False:
        return redirect('/')
    dict_obj = {'new_review_count': get_un_viewed_reviews_count(False),
                'reg_request_count': get_service_requests(False).count(),
                }
    if request.GET.get('new'):
        return render(request, 'admin-group-of-price-edit.html', dict_obj)

    elif request.GET.get('edit'):
        dict_obj = {'new_review_count': get_un_viewed_reviews_count(False),
                    'reg_request_count': get_service_requests(False).count(),
                    'group': get_group_of_service(request.GET.get('group_id'))}
        return render(request, 'admin-group-of-price-edit.html', dict_obj)

    elif request.GET.get('save'):
        if request.GET.get('group_id'):
            save_group_of_service(group_id=request.GET.get('group_id'), name=request.GET.get('name'))
            return redirect('price-moderation')
        else:
            save_group_of_service(group_id=None, name=request.GET.get('name'))
            return redirect('price-moderation')

    return render(request, 'admin-group-of-price-edit.html', dict_obj)


def admin_reg_request(request):
    """Вывод заявок на оказание услуги"""
    if is_logged(request) is False:
        return redirect('/')
    dict_obj = {'new_review_count': get_un_viewed_reviews_count(False),
                'reg_request_count': get_service_requests(False).count(),
                'requests_pending': get_service_requests(False),
                'requests_processed': get_service_requests(True), }
    return render(request, 'admin-reg-request.html', dict_obj)


def admin_request_processed(request):
    """Пометить заявку как отработанную"""
    if is_logged(request) is False:
        return redirect('/')
    processed_request(request.GET['req_id'])
    return redirect('reg-request')


def admin_report_services(request):
    """Отчет об оказанных услугах"""
    if is_logged(request) is False:
        return redirect('/')
    if request.GET.get('date_start') and request.GET.get('date_end'):
        dict_obj = {'new_review_count': get_un_viewed_reviews_count(False),
                    'reg_request_count': get_service_requests(False).count(),
                    'report': report_services(request.GET.get('date_start'), request.GET.get('date_end')),
                    'date_start': request.GET.get('date_start'),
                    'date_end': request.GET.get('date_end'), }
    else:
        dict_obj = {'new_review_count': get_un_viewed_reviews_count(False),
                    'reg_request_count': get_service_requests(False).count(),
                    'report': report_services(datetime.date(2020, 1, 1), datetime.date(2099, 1, 1)), }
    return render(request, 'admin-report-services.html', dict_obj)


def home(request):
    return redirect('clients')


def admin_logout(request):
    logout(request)
    return redirect('/')


def admin_login(request):
    """Авторизация"""
    if is_logged(request) is True:
        return redirect('home')
    if request.POST.get('username') and request.POST.get('password'):
        login(request, request.POST.get('username'), request.POST.get('password'))
        return redirect('login')
    dict_obj = {}
    return render(request, 'admin_login.html', dict_obj)


