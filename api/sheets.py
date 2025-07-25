import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up the scope and authenticate with your service account
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('gspread-creds.json', scope)
client = gspread.authorize(credentials)

# Open the spreadsheet
SHEET_NAME = 'YourGoogleSheetName'  # <-- Replace this with your actual Google Sheet name
sheet = client.open(SHEET_NAME).sheet1  # Assumes you're working with the first sheet

# -------------------------
# Fetch a row for a given status
# -------------------------
def get_next_contact():
    rows = sheet.get_all_records()
    for i, row in enumerate(rows, start=2):  # start=2 to skip header
        if row.get('Status', '').lower() == 'pending':
            return {
                "row_index": i,
                "name": row.get("Name"),
                "phone": row.get("Phone"),
                "location": row.get("Location"),
            }
    return None

# -------------------------
# Update the call status of a row
# -------------------------
def update_status(row_index, status):
    sheet.update_cell(row_index, 4, status)  # Assuming 'Status' is in column D (4)

# -------------------------
# Append a new contact (optional helper)
# -------------------------
def add_contact(name, phone, location, status="Pending"):
    sheet.append_row([name, phone, location, status])
