from typing import List
from sources.Source import Source
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


class DriveEngine(Source):
    def __init__(self, config: dict, name: str, priority: int = 0) -> None:
        super().__init__(config, name, priority)

    async def _search(self, query: str) -> List[Result]:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.sync_search, query)

    def sync_search(self, query: str) -> List[Result]:
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
        return list(res)
