from django.shortcuts import render, HttpResponse
from django.core.paginator import Paginator
from django.conf import settings
import os
import csv
import google_photos.management.commands.load_photos as load_photos

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

def gdrive_webhook(request):
    load_photos.loadAlbums()
    return HttpResponse("OK")

def photo_gallery(request):
    if not load_photos.loading:
        try:
                return render(request, 'photo_gallery.html', {
                        'page_title': 'Album',
                        'urls':loadUrls("119XURZ4AGwTAhpU5HTu8MuAqBB76NB0e")
                        })
        except Exception:
                return render(request, 'photo_gallery_maintenance.html', {})
    else:
        return render(request, 'photo_gallery_maintenance.html', {})
        


def photo_gallery_home(request):
    if not load_photos.loading:
        try:
                return render(request, 'photo_gallery_home.html', {
                        'page_title': 'Photo Gallery',
                        'albums':loadAlbums()
                        })
        except Exception:
                return render(request, 'photo_gallery_maintenance.html', {})
    else:
        return render(request, 'photo_gallery_maintenance.html', {})
