from django.shortcuts import render
from django.core.paginator import Paginator
from django.conf import settings

def home(request, errors=None, notifications=None):
    errors = errors or []
    notifications = notifications or []

    return render(request, 'home.html', {
        'page_title': 'home',
        # 'sidebar_item': 'home',
        'errors': errors,
        'notifications':notifications,
        'login_redirect_to' : '/',
        })

# def search(request):
#     search_results = []
#     if request.GET and 'q' in request.GET and request.GET['q']:
#         search_results = [item for item in News.pubs_objects.filter(title__icontains=request.GET['q'])] + \
#                          [item2 for item2 in News.pubs_objects.filter(body__icontains=request.GET['q'])]

#     return render(request, 'search.html', {
#         'page_title': 'Search Result',
#         'search_results': search_results
#     })