from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys
from django.core.management.base import BaseCommand, CommandError
from local_settings import CLIENT_ID,CLIENT_SECRET


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        loadAlbums()

loading = False
shouldRepeat = False

def loadAlbums():
    global loading
    global shouldRepeat
    if loading:
        shouldRepeat = True
        return
    
    loading = True
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    dirname = os.path.dirname(__file__)
    token_path = os.path.join(dirname, 'token.pickle')
    cred_path = os.path.join(dirname, 'credentials.json')

    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
            print(creds.token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                cred_path, SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    albums_path = os.path.join(dirname, '../../albums.csv')

    with open(albums_path, 'w') as f:
        f.write("")

    rootFolder = "1hnoUcsxODd22-Vauz8zjWhIRvW9JkERJ"
    loadFiles(rootFolder, service, "root")

    loading = False  
    if shouldRepeat:
        shouldRepeat = False
        loadAlbums()

def loadFiles(folderId, service, name):
    results = service.files().list(
        pageSize=100,
        orderBy="name",
        fields="nextPageToken, files(id, name, webContentLink, mimeType)",
        q="'{0}' in parents".format(folderId)
    ).execute()

    dirname = os.path.dirname(__file__)
    album_path = os.path.join(dirname, "../../album-{albumId}.csv".format(albumId=folderId))
    with open(album_path, 'w') as f:
        counter = 1
        while True:
            for item in results.get('files', []):
                if item["mimeType"].startswith("image"):
                    f.write("https://drive.google.com/a/fbk.eu/uc?id={0},{1}\n".format(item["id"], counter))
                    counter += 1
                    
                    sys.stdout.write("\rLoaded {0} files from {1}".format(counter, name))
                    sys.stdout.flush()

                elif item["mimeType"].startswith("application/vnd.google-apps.folder"):
                    albums_path = os.path.join(dirname, "../../albums.csv")
                    with open(albums_path, 'a') as f:
                        f.write("{},{}\n".format(item["id"],item["name"]))
                    loadFiles(item["id"], service, item["name"])

            pageToken = results.get('nextPageToken', '')
            if pageToken == '':
                break

            results = service.files().list(
                pageSize=100,
                orderBy="name",
                fields="nextPageToken, files(id, name, webContentLink, mimeType)",
                q="'{0}' in parents".format(folderId),
                pageToken=pageToken
            ).execute()