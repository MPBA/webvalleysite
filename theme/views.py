from django.shortcuts import render
from django.core.paginator import Paginator
from django.conf import settings
import os
import csv

def home(request, errors=None, notifications=None):
    errors = errors or []
    notifications = notifications or []

    return render(request, 'index.html', {
        'page_title': 'home',
        # 'sidebar_item': 'home',
        'errors': errors,
        'notifications':notifications,
        'login_redirect_to' : '/',
        })

def loadUrls():
    with open('./google_photos/album-AMBQJJKPmTQXBgijCw3uqPpIprQL3E-lT69ymYzqiz38ynUHLUpnX7b0V1NRAa_YAErQsPepYrg0.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        return list(reader)

def photo_gallery(request):
    return render(request, 'photo_gallery.html', {
            'page_title': 'Photo Gallery',
            'urls':loadUrls()
    	})
