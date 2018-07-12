from apiclient.discovery import build
from oauth2client import file, client, tools


# Setup the Sheets API
def create_google_api():
    CLIENT_SECRET = 'client_secret.json'
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPES)
        creds = tools.run_flow(flow, store)

#Retrieves a list of list from the google sheet
def retrieve_sheet_info(key):
    service = build('sheets', 'v4', developerKey=key)
    spreadsheet_ID = 'sheet ID here'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_ID, range='Sheet1!A2:C12').execute()
    numRows = result.get('values') if result.get('values')is not None else 0
    return numRows





