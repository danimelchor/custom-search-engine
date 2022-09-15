from custom_types import Result
from sources.Base import Base
import aiohttp
import ssl
import certifi


class NotionEngine(Base):
    def __init__(self, config: dict, name: str):
        super().__init__(config, name)
        self.config = config
        self.url = config["notion"]["url"]
        self.token = config["notion"]["api_key"]

    async def search(self, query: str) -> None:
        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

        payload = {
            "query": query,
            "sort": {"direction": "ascending", "timestamp": "last_edited_time"},
            "page_size": 100,
        }

        ssl_context = ssl.create_default_context(cafile=certifi.where())
        conn = aiohttp.TCPConnector(ssl=ssl_context)

        async with aiohttp.ClientSession(connector=conn) as session:
            async with session.post(
                self.url, json=payload, headers=headers
            ) as response:
                if response.status == 200:
                    res_json = await response.json()
                    res_results = res_json["results"][: self.max_results]

                    res = []
                    for r in res_results:
                        # Ensure title exists
                        if (
                            "Name" in r["properties"]
                            and "title" in r["properties"]["Name"]
                            and len(r["properties"]["Name"]["title"]) > 0
                            and "plain_text" in r["properties"]["Name"]["title"][0]
                        ):
                            res.append(
                                Result(
                                    title=r["properties"]["Name"]["title"][0][
                                        "plain_text"
                                    ],
                                    action="open_browser",
                                    action_args=f"notion://{r['url']}",
                                    type="notion",
                                )
                            )
                    self._save_results(res, query)
