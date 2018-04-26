from django.core.management.base import BaseCommand

from alumni.models import AlumniStudent
from timetable.googleoauth import authenticate_google_docs


GOOGLE_MAPS_API_URL = 'http://maps.googleapis.com/maps/api/geocode/json'

SPREADSHEET, WORKSHEET = 'WV-studenti-2001_2017', 'NOW_TO_DB'

NOME, COGNOME = 'NOME', 'COGNOME'
LATITUDINE, LONGITUDINE = 'latitudine', 'longitudine'
ANNO = 'ANNO WV'
EMAIL = 'email'
PROVENIENZA = 'provenienza'
POSIZIONE_ATTUALE = 'posizione attuale'
DESCRIZIONE = 'descrizione'


class Command(BaseCommand):
    help = "Carica gli alumni dallo spreadsheet su gdrive," \
           "dando la priorita' a quello che gia' c'e' sul db"

    def handle(self, *args, **options):
        gc = authenticate_google_docs()
        s = gc.open(SPREADSHEET)
        rows = s.worksheet(WORKSHEET).get_all_records()

        print 'Importing alumni from %s' % SPREADSHEET

        for row in rows:
            # cerca un alumni che ha quel nome, cognome e anno. Se non c'e'
            # crealo. Non ho usato l'email perche' potrebbe essere cambiata
            alumni, created = AlumniStudent.objects.get_or_create(
                name='%s %s' % (row[NOME], row[COGNOME]),
                year_in_school=row[ANNO],
                defaults={
                    'lat': 0,  # lat e lon tocca farli a mano, le api di google
                    'lon': 0,  # throttlano dopo pochissime richieste
                    'approved': False,
                    'desc': '',
                    'email': row[EMAIL],
                    'loc_string': row[POSIZIONE_ATTUALE] or row[PROVENIENZA]
                }
            )

            print 'Alumni %s %s' % (alumni, 'succesfully loaded' if created else 'skipped. Already in DB')
            raw_input('Press enter for the next one')
