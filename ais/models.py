import datetime as datetime
from django.db import models


class Client(models.Model):
    """Информация о клиенте"""
    fio = models.CharField(max_length=200, verbose_name='ФИО')
    address = models.CharField(max_length=200, verbose_name='Адрес')
    birth_day = models.DateField(verbose_name='Дата рождения')
    work_place = models.CharField(max_length=200, verbose_name='Место работы')
    phone = models.CharField(max_length=13, verbose_name='Телефон')

    def __str__(self):
        return str(self.id)


class GroupService(models.Model):
    """Группа услуг"""
    name = models.CharField(max_length=200, verbose_name='Наименование')
    num_order = models.IntegerField(verbose_name="Порядковый номер", null=True)

    def __str__(self):
        return str(self.id)


class Service(models.Model):
    """Услуги"""
    group = models.ForeignKey(GroupService, on_delete=models.CASCADE, verbose_name='Группа услуг')
    name = models.CharField(max_length=200, verbose_name='Наименование')
    price = models.DecimalField(default=0, max_digits=15, decimal_places=10, verbose_name='Цена')

    def __str__(self):
        return str(self.id)

#
# class TypeOfMaterial(models.Model):
#     """Типы материалов"""
#     name = models.CharField(max_length=200, verbose_name='Наименование')
#
#     def __str__(self):
#         return str(self.id)
#
#
# class Material(models.Model):
#     """Материалы"""
#     type = models.ForeignKey(TypeOfMaterial, on_delete=models.CASCADE, verbose_name='Тип материала')
#     name = models.CharField(max_length=200, verbose_name='Наименование')
#
#     def __str__(self):
#         return str(self.id)
#
#
# class TypeOfTool(models.Model):
#     """Типы инструментов"""
#     name = models.CharField(max_length=200, verbose_name='Наименование')
#
#     def __str__(self):
#         return str(self.id)
#
#
# class Tool(models.Model):
#     """Инструменты"""
#     type = models.ForeignKey(TypeOfTool, on_delete=models.CASCADE, verbose_name='Тип инструмента')
#     name = models.CharField(max_length=200, verbose_name='Наименование')
#
#     def __str__(self):
#         return str(self.id)


class RequestService(models.Model):
    """Заявки на прием"""
    fio = models.CharField(max_length=200, verbose_name='ФИО')
    phone = models.CharField(max_length=13, verbose_name='Телефон')
    info = models.TextField(verbose_name='Дополнительная информация')
    date = models.DateTimeField(default=datetime.datetime.now(), verbose_name='Дата и время заявки')
    processed = models.BooleanField(default=False, verbose_name='Заявка обработана')

    def __str__(self):
        return str(self.id)


class UserAIS(models.Model):
    """Пользователь АИС"""
    fio = models.CharField(max_length=200, verbose_name='ФИО')
    login = models.CharField(verbose_name='Логин', max_length=20)
    password = models.CharField(max_length=20, verbose_name='Пароль')

    def __str__(self):
        return str(self.id)


class Photo(models.Model):
    """Фото до/после"""
    # user = models.ForeignKey(UserAIS, on_delete=models.CASCADE)
    photo_before = models.ImageField(verbose_name='Фото до', upload_to='photo_works/')
    photo_after = models.ImageField(verbose_name='Фото после', upload_to='photo_works/')
    description = models.CharField(max_length=100, verbose_name='Описание')
    date_create = models.DateTimeField(default=datetime.datetime.now(), verbose_name='Дата создания')

    def __str__(self):
        return str(self.id)


class Review(models.Model):
    """Отзывы"""
    user = models.ForeignKey(UserAIS, on_delete=models.CASCADE, null=True)
    caption = models.CharField(max_length=200, verbose_name='Подпись')
    datetime = models.DateTimeField(default=datetime.datetime.now(), verbose_name='Дата и время')
    text = models.TextField(verbose_name='Текст отзыва')
    approved = models.BooleanField(default=False, verbose_name='Одобрено')
    viewed = models.BooleanField(default=False, verbose_name='Просмотрено')

    def __str__(self):
        return str(self.id)


class Promotion(models.Model):
    """Акции"""
    user = models.ForeignKey(UserAIS, on_delete=models.CASCADE)
    date_start = models.DateField(verbose_name='Дата начала')
    date_end = models.DateField(verbose_name='Дата окончания')
    text = models.TextField(verbose_name='Текст объявления')

    def __str__(self):
        return str(self.id)


# class InvoiceMaterial(models.Model):
#     """Поступление / списание материалов материалов"""
#     TYPE_CONSUMPTION = '0'
#     TYPE_RECEIPT = '1'
#
#     user = models.ForeignKey(UserAIS, on_delete=models.CASCADE)
#     material = models.ForeignKey(Material, on_delete=models.CASCADE)
#     count = models.IntegerField(verbose_name='Количество')
#     type = models.CharField(max_length=1, verbose_name='Тип операции')
#     date = models.DateField(verbose_name='Дата')
#
#     def __str__(self):
#         return str(self.id)
#
# #
# class InvoiceTool(models.Model):
#     """Поступление / списание инструментов"""
#     TYPE_CONSUMPTION = '0'
#     TYPE_RECEIPT = '1'
#
#     user = models.ForeignKey(UserAIS, on_delete=models.CASCADE)
#     tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
#     count = models.IntegerField(verbose_name='Количество')
#     type = models.CharField(max_length=1, verbose_name='Тип операции')
#     date = models.DateField(verbose_name='Дата')
#
#     def __str__(self):
#         return str(self.id)


class CustomerReception(models.Model):
    """Прием клиента"""
    user = models.ForeignKey(UserAIS, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    datetime = models.DateTimeField(default=datetime.datetime.now(), verbose_name='Дата и время приема')
    note = models.TextField(verbose_name='Заметка')

    def __str__(self):
        return str(self.id)

#
# class UsedMaterial(models.Model):
#     """Использованные материалы при приеме"""
#     reception = models.ForeignKey(CustomerReception, on_delete=models.CASCADE, verbose_name='Код приема')
#     material_invoice = models.ForeignKey(InvoiceMaterial, on_delete=models.CASCADE,
#                                          verbose_name='Код расхода материала')
#
#     def __str__(self):
#         return str(self.id)


class ServicesProvided(models.Model):
    """Оказанные услуги при приеме"""
    reception = models.ForeignKey(CustomerReception, on_delete=models.CASCADE, verbose_name='Код приема')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, verbose_name='Код услуги', null=True)
    price = models.DecimalField(verbose_name='Стоимость', max_digits=15, decimal_places=10)

    def __str__(self):
        return str(self.id)


# class Contacts(models.Model):
#     """Контакты"""
#     city = models.CharField(max_length=30, verbose_name='Город')
#     address = models.CharField(max_length=100, verbose_name='Улица - Дом')
#     phone_one = models.CharField(max_length=12, verbose_name='Телефон 1')
#     phone_two = models.CharField(max_length=12, verbose_name='Телефон 2')
#     schedule_days = models.CharField(max_length=20, verbose_name='График работы - дни')
#     schedule_hours = models.CharField(max_length=20, verbose_name='График работы - часы')
