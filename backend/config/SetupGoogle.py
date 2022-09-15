from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/drive.metadata.readonly']

def get_abs(file):
    current_abs_path = os.path.abspath(__file__)
    return os.path.join(os.path.dirname(current_abs_path), file)
    

def get_google_creds():
    creds = None

    # Get absolute paths
    google_token_path = get_abs('./google_token.json')
    google_path = get_abs('./google.json')

    if os.path.exists(google_token_path):
        creds = Credentials.from_authorized_user_file(google_token_path, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token: creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                google_path, SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(google_token_path, 'w') as token:
            token.write(creds.to_json())

    return creds