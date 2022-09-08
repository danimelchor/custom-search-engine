from typing import List
from sources.Base import Base
from custom_types import Result

from config.SetupGoogle import get_google_creds

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class DriveEngine(Base):
  def __init__(self, config: dict) -> None:
    super().__init__(config)

  def search(self, query: str) -> List[Result]:
    creds = get_google_creds()
    files = []

    try:
        service = build('drive', 'v3', credentials=creds)
        response = service.files().list(
          q=f"name contains '{query}'",
          spaces='drive',
          fields='files(name, webViewLink, mimeType)'
        ).execute()
        files = response.get('files', [])[:5]
    except HttpError as error:
        print(F'An error occurred: {error}')

    res = map(lambda x: Result(
      title=x["name"],
      url=x["webViewLink"],
      type=x["mimeType"],
      source="Google Drive"
    ), files)
    return list(res)