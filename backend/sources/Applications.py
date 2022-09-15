from typing import List
from sources.Base import Base
from custom_types import Result
import os, asyncio


class ApplicationsEngine(Base):
    def __init__(self, config: dict, name: str, priority: int = 0) -> None:
        super().__init__(config, name, priority)

    async def _search(self, query: str) -> List[Result]:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.sync_search, query)

    def sync_search(self, query: str) -> List[Result]:
        res = []
        for app in os.listdir("/Applications"):
            if query in app.lower():
                res.append(
                    Result(
                        title=app.replace(".app", "").capitalize(),
                        action="open_app",
                        action_args="/Applications/" + app,
                        type="app",
                    )
                )

                if len(res) >= self.max_results:
                    return res
        return res
