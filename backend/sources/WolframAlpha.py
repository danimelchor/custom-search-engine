from typing import List
from custom_types import Result
from sources.Source import Source
import aiohttp


class WolframAlphaEngine(Source):
    def __init__(self, config: dict, name: str, priority: int = 0) -> None:
        super().__init__(config, name, priority)
        self.units = config["units"]
        self.url = config["wolfram_alpha"]["url"]
        self.app_id = config["wolfram_alpha"]["app_id"]

    async def _search(self, query: str) -> List[Result]:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.url,
                params={
                    "appid": self.app_id,
                    "input": query,
                    "output": "json",
                    "units": self.units,
                    "format": "plaintext",
                },
            ) as res:
                res_json = await res.json()

                pods = res_json["queryresult"]["pods"]
                text_results = []

                for pod in pods:
                    for subpod in pod["subpods"]:
                        text = subpod["plaintext"].strip()

                        if text:
                            text_results.append(text)

                rs = map(
                    lambda x: Result(
                        title=x,
                        action="open_browser",
                        action_args=f"wolframalpha.com/input?i={query}",
                        type="wolframalpha",
                    ),
                    text_results,
                )

                return list(rs)
