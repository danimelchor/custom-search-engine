from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/drive.metadata.readonly']

def get_google_creds():
  creds = None
  if os.path.exists('config/google_token.json'):
      creds = Credentials.from_authorized_user_file('config/google_token.json', SCOPES)

  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token: creds.refresh(Request())
      else:
          flow = InstalledAppFlow.from_client_secrets_file(
              'config/google.json', SCOPES)
          creds = flow.run_local_server(port=0)
      with open('config/google_token.json', 'w') as token:
          token.write(creds.to_json())

  return creds