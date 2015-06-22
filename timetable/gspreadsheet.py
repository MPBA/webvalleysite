# Taken from: https://gist.github.com/1650271

import re, urllib, urllib2, json
import gspread


class Spreadsheet(object):
    def __init__(self, key):
        super(Spreadsheet, self).__init__()
        self.key = key


class Client(object):
    def __init__(self, email, password):
        super(Client, self).__init__()
        self.email = email
        self.password = password
        self.gc = gspread.login(self.email, self.password)

    #
    # def _get_auth_token(self, email, password, source, service):
    #     url = "https://www.google.com/accounts/ClientLogin"
    #     print email, password, source, service
    #     params = {
    #         "Email": email, "Passwd": password,
    #         "service": service,
    #         "accountType": "HOSTED_OR_GOOGLE",
    #         "source": source
    #     }
    #     req = urllib2.Request(url, urllib.urlencode(params))
    #     return re.findall(r"Auth=(.*)", urllib2.urlopen(req).read())[0]
    #
    # def get_auth_token(self):
    #     source = type(self).__name__
    #     return self._get_auth_token(self.email, self.password, source, service="wise")

    def download(self, spreadsheet, gid=0, format="csv"):
        dev_key = 'AIzaSyC13P3RmTltG7hUZG_TsfDtIxNLlxT8MlY'
        json_url = 'https://www.googleapis.com/drive/v2/files/%s?key=%s' % (spreadsheet.key, dev_key)
        req = urllib2.Request(json_url)

        res = urllib2.urlopen(req)
        j = json.loads(res.read())

        req = urllib2.Request(j["exportLinks"]["text/csv"] + "&gid=%s" % gid)

        return urllib2.urlopen(req)


if __name__ == "__main__":
    import getpass
    import csv

    email = ""  # (your email here)
    password = getpass.getpass()
    spreadsheet_id = ""  # (spreadsheet id here)

    # Create client and spreadsheet objects
    gs = Client(email, password)
    ss = Spreadsheet(spreadsheet_id)

    # Request a file-like object containing the spreadsheet's contents
    csv_file = gs.download(ss)

    # Parse as CSV and print the rows
    for row in csv.reader(csv_file):
        print ", ".join(row)

