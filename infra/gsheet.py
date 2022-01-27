from oauth2client.service_account import ServiceAccountCredentials

import gspread

# Need to give the sheep google bot permission
sheet_name = 'CF EPGP'

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
sheet = client.open(sheet_name)


def get_epgp_from_gsheet():
    # Sheet index 0
    sheet_instance = sheet.get_worksheet(0)
    records_data = sheet_instance.get_all_records()
    return records_data


def get_loot_from_gsheet():
    # Sheet index 4
    sheet_instance = sheet.get_worksheet(4)
    records_data = sheet_instance.get_all_records()
    return records_data
