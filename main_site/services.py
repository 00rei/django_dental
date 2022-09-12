import datetime
import math


from ais.models import *
from ais.sendmessage import sendTelegram


def register_a_service_request(fio, phone, info):
    req = RequestService(fio=fio, phone=phone, info=info)
    sendTelegram(fio=fio, phone=phone, text=info)
    req.save()
    return None


def save_review(fio, info):
    review = Review(caption=fio, text=info)
    review.save()
    return None


def get_reviews_to_feedback_list(page):
    review_list = get_approved_reviews((page - 1) * 10, page * 10)
    return review_list


def get_count_pages_approved_reviews():
    return math.ceil(Review.objects.all().count() / 10)


def get_approved_reviews(start, end):
    review_list = Review.objects.all().filter(approved=True).order_by('-datetime')[start:end]
    return review_list


def get_approved_reviews_three_in_a_row(count):
    reviews = get_approved_reviews(3, count)
    return_list = []
    a_list = []
    i = 0
    for rev in reviews:
        a_list.append(rev)
        i += 1
        if i % 3 == 0:
            return_list.append(a_list[:])
            a_list.clear()

    if i % 3 != 0:
        return_list.append(a_list[:])

    return return_list


def get_active_promotions():
    return Promotion.objects.filter(date_end__gte=datetime.date.today(), date_start__lte=datetime.date.today())

