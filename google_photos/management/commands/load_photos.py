import httplib2
import sys

from googleapiclient.discovery import build
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from django.core.management.base import BaseCommand, CommandError
from local_settings import CLIENT_ID,CLIENT_SECRET

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        scope = 'https://www.googleapis.com/auth/photoslibrary'

        flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, scope)

        storage = Storage('credentials.dat')

        credentials = storage.get()

        if credentials is None or credentials.invalid:
            credentials = tools.run_flow(flow, storage)

        print("loaded credentials")

        http = httplib2.Http()
        http = credentials.authorize(http)

        print("preparing api")
        service = build('photoslibrary', 'v1', http=http)

        try:

            print("loading albums")
            albums = service.albums().list(pageSize=50,
                                        fields="nextPageToken,albums(id,title,coverPhotoBaseUrl)").execute().get('albums', [])

            print ("loading images")
            with open("google_photos/albums.csv",'w') as albumFile:
                for album in albums:
                    albumFile.write(album['id'])

                    query = {
                        "pageSize": "100",
                        "albumId": album['id'],
                    }
                    request = service.mediaItems().search(
                        body=query, fields="nextPageToken,mediaItems(id,baseUrl,mimeType)")

                    i = 1
                    with open("google_photos/album-{albumId}.csv".format(albumId=album['id']), 'w') as f:
                        while True:
                            response = request.execute()
                            for image in response.get('mediaItems', []):
                                if image['mimeType'].startswith("image"):
                                    f.write("{baseUrl},{i}\n".format(
                                        baseUrl=image['baseUrl'], i=i))
                                    i += 1

                            if response.get('nextPageToken', '') == '':
                                break
                            query = {
                                "pageSize": "100",
                                "albumId": album['id'],
                                "pageToken": response.get('nextPageToken', '')
                            }

                            request = service.mediaItems().search(
                                body=query, fields="nextPageToken,mediaItems(id,baseUrl,mimeType)")

        except AccessTokenRefreshError:
            print ('The credentials have been revoked or expired, please re-run'
                'the application to re-authorize')
