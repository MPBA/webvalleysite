from django import template
from staticcontent.models import StaticPage
register = template.Library()

@register.inclusion_tag('sidebar.html', takes_context=True)
def sidebar(context, selected_item):
    '''
    Generates the sidebar, including the links to the static pages.
    '''
    static_pages_list = [page for page in StaticPage.objects.all().order_by('sidebar_index') if page.public]
    request = context['request']
    user = request.user

    return {'static_pages_list': static_pages_list, 'selected': selected_item, 'user': user }
