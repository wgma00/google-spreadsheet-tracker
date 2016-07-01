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
import requests
import json
import yaml
import time
from oauth2client.service_account import ServiceAccountCredentials


class Database(object):
    def __init__(self):
        '''(Database) -> None'''
        with open("details.yaml", 'r') as yaml_file:
           self.details = yaml.load(yaml_file)
           self.torn_api_key = str(self.details['torn_api_key'])
           self.google_creds_path = str(self.details['google_creds_path'])
           self.google_sheets_key = str(self.details['google_sheets_key'])
           self.user_ids = self.details['user_ids']
           self.userbase = self.details['userbase'] if self.details['userbase'] != None else {user:{} for user in self.user_ids}
           self.updateDatabase()
           self.wks = None
           self.googleSpreadSheetSetup()
           self.uploadToSpreadSheet()

    def googleSpreadSheetSetup(self):
        '''(Database)->None
            Opens the spread sheet at the specified key 
        '''
        self.scope = ['https://spreadsheets.google.com/feeds']
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.google_creds_path, self.scope)
        self.gc = gspread.authorize(self.credentials)
        self.wks = self.gc.open_by_key(self.google_sheets_key).sheet1

    def uploadToSpreadSheet(self):
        '''(Database) -> None
            Here we will upload all the information gained from the torn api
            into a google spreadsheet
        '''
        pass
        # days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        # month = int(time.strftime("%d/%m/%Y").split('/')[1])-1
        # top_row = ['Users'] + ['Day: ' + str(i) for i in range(1, days_in_month[month]+1)]
        # print(top_row)
        # for i in range(len(top_row)):
        #     self.wks.update_acell('A'+str(i+1), top_row[i])

        # for user in range(len(self.user_ids)):
        #     self.wks.update_acell( chr(ord('B')+i)+'1', self.user_ids[user])
        #     # for day in range(1, days_in_month[month]+1):
        #     #     if self.userbase[user][day] == None:
        #     #         self.wks.update_acell(chr(ord('B')+user)+str(day), userbase[user][day]['xantaken'])


    def updateDatabase(self):
        '''(Database) -> None
           Updates user information with the most recent information, should be
           done daily
        '''
        date = time.strftime("%d/%m/%Y").split('/')[0]
        for user in self.userbase:
            r = requests.request("GET", "https://api.torn.com/user/"+user+"?selections=personalstats&key="+self.torn_api_key)
            data = r.json()
            self.userbase[user][date] = data
        # write the changes to file
        self.details['userbase'] = self.userbase 
        with open('details.yaml', 'w') as outfile:
            outfile.write( yaml.dump(self.details, default_flow_style=False))


if __name__ == '__main__':
    d = Database()
