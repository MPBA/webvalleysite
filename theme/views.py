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

def loadUrls(id):
    with open('./google_photos/album-{}.csv'.format(id), 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        return list(reader)

def loadAlbums():
    with open('./google_photos/albums.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        albums = list(reader)
        populatedAlbums = []

        for id, name in albums:
            thumbnail = loadUrls(id)[0][0]
            populatedAlbums.append([id,name,thumbnail])
        return populatedAlbums


def photo_gallery(request):
    return render(request, 'photo_gallery.html', {
            'page_title': 'Album',
            'urls':loadUrls("119XURZ4AGwTAhpU5HTu8MuAqBB76NB0e")
    	})

def photo_gallery_home(request):
    return render(request, 'photo_gallery_home.html', {
            'page_title': 'Photo Gallery',
            'albums':loadAlbums()
    	})
