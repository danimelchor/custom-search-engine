from typing import List
from sources.Base import Base
from custom_types import Result
import os, re, asyncio

from const import IGNORED_FOLDERS, ROOTS_TO_LOOK_IN


class FolderEngine(Base):
    def __init__(self, config: dict, name: str) -> None:
        super().__init__(config, name)

    def _ignore_dirs(self, dirs: list) -> list:
        return list(filter(lambda d: self._should_use_dir(d), dirs))

    def _should_use_dir(self, name: str) -> bool:
        return re.match(IGNORED_FOLDERS, name, re.IGNORECASE) is None

    async def search(self, query: str) -> None:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.sync_search, query)

    def sync_search(self, query: str) -> None:
        res = []
        for root in ROOTS_TO_LOOK_IN:
            for curr, dirs, _ in os.walk(root):
                dirs[:] = self._ignore_dirs(dirs)

                for dir in dirs:
                    if query in dir:
                        res.append(
                            Result(
                                title=os.path.join(curr, dir) + "/",
                                action="open_finder",
                                action_args=os.path.join(curr, dir),
                                type="folder",
                            )
                        )

                        if len(res) >= self.max_results:
                            return self._save_results(res, query)

        self._save_results(res, query)
