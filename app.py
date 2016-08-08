# The MIT License (MIT)
# 
# Copyright (c) 2016 William Granados
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import gspread
import yaml
from oauth2client.service_account import ServiceAccountCredentials


class SpreadSheetTracker(object):
    """ Handles getting user data and uploading to a google spreadsheet.

    Uses the google sheets api to access and upload data.

    Attributes:
        details: map, maps variables to sensitive information.
        torn_api_key: string, api key provided by torn.
        google_creds_path: string, path to the credentials i.e. "*.json".
        google_sheets_key: string, code given to a google spreadsheet.
        wks: worksheet object, object representing the online spreadsheet.
    """
    def __init__(self):
        """Initializes basic contents required to access the service."""
        with open("details.yaml", 'r') as yaml_file:
           self.details = yaml.load(yaml_file)
           self.google_creds_path = str(self.details['google_creds_path'])
           self.google_sheets_key = str(self.details['google_sheets_key'])
           self.wks = None
           self.googleSpreadSheetSetup()
           self.modifySpreadSheet()

    def googleSpreadSheetSetup(self):
        """Authenticates user into google services and accesses spreadsheet."""
        self.scope = ['https://spreadsheets.google.com/feeds']
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.google_creds_path, self.scope)
        self.gc = gspread.authorize(self.credentials)
        self.wks = self.gc.open_by_key(self.google_sheets_key).sheet1

    def modifySpreadSheet(self):
        """Modifies spreadsheet"""
        # please refer to https://github.com/burnash/gspread for api details
        # related to modifying spreadsheets
        pass


if __name__ == '__main__':
    sst = SpreadSheetTracker()

