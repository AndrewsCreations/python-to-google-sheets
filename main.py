import os
import google.auth.transport.requests

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# https://docs.google.com/spreadsheets/d/{THIS_VALUE}/edit?gid=0#gid=0
SPREADSHEET_ID = '1Zuh2pr0RGI7UGyY1izAmtLcbjg3rJ8zpKzzH2ircc4M'

def main():
    credentials = None
    # Authorizing use of the api
    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            request = google.auth.transport.requests.Request()
            credentials.refresh(request)
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            credentials = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())

    # Spreadsheet operations 
    try:
        service = build('sheets', 'v4', credentials=credentials)
        sheets = service.spreadsheets()

        # ! Get values and print them from A2:C6 for sheet named Sheet1
        result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range='Sheet1!A2:C6').execute()

        print(result)

        values = result.get('values', [])
        for row in values:
            print(row)

        # ! Get values from A2:B6 for sheet named test
        result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range='Test!A2:B6').execute()
        
        # ! Update row values
        sheets.values().update(spreadsheetId=SPREADSHEET_ID, range='Sheet1!A8', valueInputOption='USER_ENTERED', body= {'values': [[1]]}).execute()
    except HttpError as error:
        print(error)

main()