import requests, gspread, os, ast
from oauth2client.client import SignedJwtAssertionCredentials


def authenticate_google_docs():
    f = file(os.path.join('/media/data/work/devel/git/webvalley/webvalleysite/timetable/WebValley2014-72837d7af4fc.p12'), 'rb')
    SIGNED_KEY = f.read()
    f.close()
    scope = ['https://spreadsheets.google.com/feeds', 'https://docs.google.com/feeds']
    credentials = SignedJwtAssertionCredentials('webvalleyfbk@gmail.com', SIGNED_KEY, scope)

    data = {
        'refresh_token' : '1/G6NjKS1sMff-sIPblMCM3nrw3Hu41tuCfKIaFs1cL_bBactUREZofsF9C7PrpE-j',
        'client_id' : '68799219595-oguekfb6ejolblop6je8gjkhh7q4b7re.apps.googleusercontent.com',
        'client_secret' : 'XRM3Z8yL0tkpNACBrQmxZjAd',
        'grant_type' : 'refresh_token',
    }

    r = requests.post('https://accounts.google.com/o/oauth2/token', data = data)
    credentials.access_token = ast.literal_eval(r.text)['access_token']

    gc = gspread.authorize(credentials)
    return gc