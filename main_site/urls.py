from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('price', views.price_list, name='price'),
    path('for-clients', views.for_clients, name='for-clients'),
    path('prevention', views.prevention, name='prevention'),
    path('contacts', views.contacts, name='contacts'),
    path('about', views.about, name='about'),
    path('request_service', views.request_service, name='request_service'),
    path('post_review', views.post_review, name='post_review'),
    path('discounts', views.discounts, name='discounts'),
    path('feedback', views.feedback, name='feedback'),
    path('agreement', views.agreement, name='agreement'),
]