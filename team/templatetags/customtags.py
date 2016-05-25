from django import template
from django.template import Library, Node, VariableDoesNotExist

register = Library()


@register.filter
def categories_dict(components):
    categories = {}
    for i in components:
        if i.category.category not in categories:
            categories[i.category.category] = []
        categories[i.category.category].append(i)

    return categories.items()
