from sources.Base import Base
from custom_types import Result
import os, asyncio


class ApplicationsEngine(Base):
    def __init__(self, config: dict, name: str) -> None:
        super().__init__(config, name)

    async def search(self, query: str) -> None:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.sync_search, query)

    def sync_search(self, query: str) -> None:
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
                    return self._save_results(res, query, priority=1)
        self._save_results(res, query, priority=1)
