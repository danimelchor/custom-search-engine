from custom_types import Result
from sources.Base import Base
import aiohttp


class WolframAlphaEngine(Base):
    def __init__(self, config: dict, name: str) -> None:
        super().__init__(config, name)
        self.units = config["units"]
        self.url = config["wolfram_alpha"]["url"]
        self.app_id = config["wolfram_alpha"]["app_id"]

    async def search(self, query: str) -> None:
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

                self._save_results(list(rs), query, priority=1)
