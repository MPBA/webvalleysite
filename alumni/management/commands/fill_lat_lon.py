import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from alumni.models import AlumniStudent

GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json?key=' + settings.GOOGLE_APIS_KEY2


def get_lat_lon(loc_string):
    result = requests.get(GOOGLE_MAPS_API_URL, params={'address': loc_string}).json()
    location = result['results'][0]['geometry']['location']
    lat, lon = location['lat'], location['lng']
    address = result['results'][0]['formatted_address']
    return address, lat, lon


class Command(BaseCommand):
    help = "Calcola lat e lon per gli alumni che non la hanno ancora"

    def handle(self, *args, **options):
        for alumni in AlumniStudent.objects.filter(lat=0).exclude(loc_string='').iterator():
            loc_string = alumni.loc_string

            while True:
                addr, lat, lon = get_lat_lon(loc_string)
                print '%s resolved to %s (%f, %f)' % (loc_string, addr, lat, lon)

                val = raw_input('Does that look right? (type n to change)')
                if val.capitalize() != 'N':
                    break

                loc_string = raw_input('Type another loc string ')

            alumni.loc_string, alumni.lat, alumni.lon = addr, lat, lon
            alumni.save()
