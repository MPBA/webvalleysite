from django import template
from django.template import Library, Node, VariableDoesNotExist

register = Library()


@register.filter
def categories_dict(components):
    categories = {}
    orders = {}
    for i in components:
        if i.category.category not in categories:
            categories[i.category.category] = []
            orders[i.category.order] = i.category.category
        categories[i.category.category].append(i)

    return [(v, categories[v]) for k, v in orders.iteritems()]
