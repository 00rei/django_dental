import datetime
import hashlib

from django.db.models import Max, Min, Sum, Count

from ais.models import *


def is_logged(request):
    if request.session.get('user_id', False):
        return True
    return False


def login(request, username, password):
    try:
        print(hashlib.md5((password + 'djdental').encode()).hexdigest())
        print('login ' + username)
        print('pass ' + password)
        user = UserAIS.objects.get(login=username)
        print(user.password)
        if user.password == hashlib.md5((password + 'djdental').encode()).hexdigest():
            request.session['user_id'] = user.id
            return True
        else:
            return False
    except:
        return False


def logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass


def get_unapproved_reviews():
    review_list = Review.objects.all().filter(user=None, approved=False).order_by('-datetime')
    return review_list


def get_un_viewed_reviews_count(to_view):
    review_list = Review.objects.all().filter(user=None, approved=False, viewed=False).order_by('-datetime')
    if to_view:
        for review in review_list:
            review.viewed = True
            review.save()
    return review_list.count()


def get_approved_reviews():
    review_list = Review.objects.all().filter(approved=True).order_by('-datetime')
    return review_list


def get_rejected_reviews():
    review_list = Review.objects.all().filter(approved=False).exclude(user=None).order_by('-datetime')
    return review_list


def process_review(review_id, user_id, solution):
    review = Review.objects.get(id=review_id)
    review.approved = solution
    review.user = UserAIS.objects.get(id=user_id)
    review.save()
    return None


def delete_review(review_id):
    review = Review.objects.get(id=review_id)
    review.delete()
    return None


def get_service_requests(processed):
    return RequestService.objects.all().filter(processed=processed).order_by('-date')


def processed_request(req_id):
    req = RequestService.objects.get(id=req_id)
    req.processed = True
    req.save()
    return None


def get_active_promotions():
    return Promotion.objects.filter(date_end__gte=datetime.date.today(), date_start__lte=datetime.date.today())


def get_planned_promotions():
    return Promotion.objects.filter(date_start__gte=datetime.date.today())


def create_promotions(date_start, date_end, text, user_id):
    promotion = Promotion(date_start=date_start, date_end=date_end, text=text, user_id=user_id)
    promotion.save()


def delete_promotions(pr_id):
    promotion = Promotion.objects.get(id=pr_id)
    promotion.delete()


def get_groups_of_service():
    groups = GroupService.objects.all().order_by('num_order', 'name')
    return groups


def get_group_of_service(group_id):
    return GroupService.objects.get(id=group_id)


def delete_service(price_id):
    service = Service.objects.get(id=price_id)
    service.delete()


def delete_group_of_service(group_id):
    group = GroupService.objects.get(id=group_id)
    group.delete()


def get_service(service_id):
    return Service.objects.get(id=service_id)


def save_service(service_id, group_id, name, price):
    service = Service(id=service_id, group_id=group_id, name=name, price=price)
    service.save()


def save_group_of_service(group_id, name):
    if not GroupService.objects.filter(id=group_id).exists():
        num_order = GroupService.objects.aggregate(Max('num_order'))['num_order__max'] + 1
        group = GroupService(name=name, num_order=num_order)
    else:
        group = GroupService.objects.get(id=group_id)
        group.name = name

    group.save()


def group_move_to(group_id, to):
    num_max = GroupService.objects.aggregate(Max('num_order'))['num_order__max']
    num_min = GroupService.objects.aggregate(Min('num_order'))['num_order__min']
    if to == 'up':
        group_one = GroupService.objects.get(id=group_id)
        num_one = group_one.num_order
        if num_one <= num_min:
            return None
        group_two = GroupService.objects.get(num_order=num_one - 1)
        group_two.num_order = num_one
        group_two.save()
        group_one.num_order = num_one - 1
        group_one.save()
    else:
        group_one = GroupService.objects.get(id=group_id)
        num_one = group_one.num_order
        if num_one >= num_max:
            return None
        group_two = GroupService.objects.get(num_order=num_one + 1)
        group_two.num_order = num_one
        group_two.save()
        group_one.num_order = num_one + 1
        group_one.save()


def save_photo(photo_before, photo_after, desc):
    Photo.objects.create(photo_before=photo_before, photo_after=photo_after, description=desc)


def get_photos():
    return Photo.objects.all().order_by('-date_create')


def photo_delete(photo_id):
    photo = Photo.objects.get(id=photo_id)
    photo.delete()


def get_clients():
    return Client.objects.all().order_by('fio')


def get_client(client_id):
    try:
        return Client.objects.get(id=client_id)
    except:
        return False


def get_client_receptions(client_id):
    client = Client.objects.get(id=client_id)
    return client.customerreception_set.all().order_by('-datetime')


def reception_delete(rec_id):
    reception = CustomerReception.objects.get(id=rec_id)
    reception.delete()


def save_client(client_id, fio, address, birth_day, work_place, phone):
    if not Client.objects.filter(id=client_id).exists():
        client = Client(fio=fio, address=address, birth_day=birth_day, work_place=work_place, phone=phone)
    else:
        client = Client.objects.get(id=client_id)
        client.fio = fio
        client.address = address
        client.birth_day = birth_day
        client.work_place = work_place
        client.phone = phone

    client.save()
    return client.id


def get_services():
    return Service.objects.all().order_by('name')


def save_reception(client_id, services, prices, note, user_id):
    reception = CustomerReception(client_id=client_id, note=note, user_id=user_id)
    reception.save()
    print(f'services {services}')
    print(f'prices {prices}')
    for i in range(0, len(services)):
        prov = ServicesProvided(reception_id=reception.id, service_id=services[i], price=prices[i])
        prov.save()


def report_services(date_start, date_end):
    serv = ServicesProvided.objects.all(). \
        values('service_id', 'service__name'). \
        annotate(prc=Sum('price'), cnt=Count('id')). \
        filter(reception__datetime__gte=date_start, reception__datetime__lte=date_end). \
        order_by('-prc')
    return serv
