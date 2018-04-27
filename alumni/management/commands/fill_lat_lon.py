import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from alumni.models import AlumniStudent

GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json?key=' + settings.GOOGLE_APIS_KEY


def get_alumni_lat_lon(alumni):
    result = requests.get(GOOGLE_MAPS_API_URL, params={'address': alumni.loc_string}).json()
    location = result['results'][0]['geometry']['location']
    lat, lon = location['lat'], location['lng']
    address = result['results'][0]['formatted_address']
    return address, lat, lon


class Command(BaseCommand):
    help = "Calcola lat e lon per gli alumni che non la hanno ancora"

    def handle(self, *args, **options):
        for alumni in AlumniStudent.objects.filter(lat=0).iterator():
            addr, lat, lon = get_alumni_lat_lon(alumni)
            print '%s resolved to %s' % (alumni.loc_string, addr)

            alumni.loc_string, alumni.lat, alumni.lon = addr, lat, lon
            alumni.save()

            raw_input()
