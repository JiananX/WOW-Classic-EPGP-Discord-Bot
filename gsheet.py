from oauth2client.service_account import ServiceAccountCredentials

import gspread

# define the scope
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'epgp_keyfile.json', scope)

# authorize the clientsheet
client = gspread.authorize(creds)

# get the instance of the Spreadsheet
sheet = client.open('CF EPGP')


def get_epgp_from_gsheet():
    # get the epgp sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(0)
    records_data = sheet_instance.get_all_records()
    return records_data


def get_loot_from_gsheet():
    # get the loot sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(1)
    records_data = sheet_instance.get_all_records()
    return records_data
