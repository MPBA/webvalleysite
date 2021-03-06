import csv

from django.shortcuts import render
from django.core.cache import cache
import gspread
import googleoauth

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import gspreadsheet as gss

from mezzanine.pages.models import Page

from django.core.urlresolvers import reverse


def display(request):
    page = Page.objects.get(slug=request.META['PATH_INFO'][1:-1])
    #raw_data = csv.reader(StringIO(_csv_get(page)))
    raw_data = _csv_get(page)
    data = []
    for row in raw_data:
        if row[1]:
            data.append({
                'date': row[0]+u', '+row[1],
                'activities': []
            })

        act = {
            'time': row[2],
            'name': row[3],
            'teachers': row[4],
            'links': []
        }
        for cell in row[5:]:
            if cell:
                if 'dropbox' in cell:
                    ext = cell.split('.')[-1]
                else:
                    ext = "WWW"
                act['links'].append({
                    'href': cell,
                    'extension': ext
                })
        data[-1]['activities'].append(act)
    return render(request, "timetable/display.html", {'data': data,
                                                      'page_title': 'Time table',
                                                      'sidebar_item': 'timetable'})


def _csv_get(page):
    """
    Return the csv file as a string, downloading it if needed.
    """
    cache_key = reverse('timetable.views.display')

    ret = cache.get(cache_key)
    if ret is not None:
        print 'hola'
        return ret
    else:
        print 'ciao'
        ret = _csv_download(page)
        cache.set(cache_key, ret, timeout=15)  # cache lasts 15 seconds
        return ret


def _csv_download(page):
    """
    Return the downloaded csv as a string.
    """
    # gc = gspread.login(page.timetable.google_user, page.timetable.google_passwd)
    gc = googleoauth.authenticate_google_docs()
    csv_file = gc.open('WebValley2019')

    # gsession = gss.Client(page.timetable.google_user, page.timetable.google_passwd)
    # ss = gss.Spreadsheet(page.timetable.spreadsheet)
    # csv_file = gsession.download(ss, gid=page.timetable.spreadsheet_gid)
    # read = csv_file.read()
    read = csv_file.worksheet('TIMETABLE').get_all_values()
    # print "csv", read
    return read
