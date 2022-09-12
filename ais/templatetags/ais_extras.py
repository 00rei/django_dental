from django import template

register = template.Library()


@register.filter(is_safe=True)
def sum_price(value):
    sum = 0
    for v in value:
        sum += v.price
    return sum


@register.filter(is_safe=True)
def sum_total_count_rep(value):
    sum = 0
    for v in value:
        sum += v['cnt']
    return sum


@register.filter(is_safe=True)
def sum_total_price_rep(value):
    sum = 0
    for v in value:
        sum += v['prc']
    return sum
