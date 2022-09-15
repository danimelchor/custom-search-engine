from typing import List
from sources.Base import Base
from custom_types import Result

from config.SetupGoogle import get_google_creds

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import asyncio


MIME_TO_TYPE = {
    "application/vnd.google-apps.document": "document",
    "application/vnd.google-apps.drawing": "drawing",
    "application/vnd.google-apps.file": "file",
    "application/vnd.google-apps.folder": "folder",
    "application/vnd.google-apps.presentation": "presentation",
    "application/vnd.google-apps.spreadsheet": "spreadsheet",
    "video/mp4": "video",
    "application/pdf": "pdf",
}


class DriveEngine(Base):
    def __init__(self, config: dict, name: str) -> None:
        super().__init__(config, name)

    async def search(self, query: str) -> None:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.sync_search, query)

    def sync_search(self, query: str) -> None:
        creds = get_google_creds()
        files = []

        try:
            service = build("drive", "v3", credentials=creds)
            response = (
                service.files()
                .list(
                    q=f"name contains '{query}'",
                    spaces="drive",
                    fields="files(name, webViewLink, mimeType)",
                )
                .execute()
            )
            files = response.get("files", [])[: self.max_results]
        except HttpError as error:
            print(f"An error occurred: {error}")

        res = map(
            lambda x: Result(
                title=x["name"],
                action="open_browser",
                action_args=x["webViewLink"],
                type=MIME_TO_TYPE[x["mimeType"]],
            ),
            files,
        )
        self._save_results(list(res), query)
