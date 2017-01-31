import requests, gspread, os, ast
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http

def authenticate_google_docs():

    path_to_json_key = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'WebValley2014-3f9dbe414b8a.json')
    scope = ['https://spreadsheets.google.com/feeds', 'https://docs.google.com/feeds']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(path_to_json_key, scopes=scope)

    gc = gspread.authorize(credentials)
    return gc

