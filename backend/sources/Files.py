from sources.Base import Base
from custom_types import Result
import os, re, asyncio

from const import IGNORED_FOLDERS, ROOTS_TO_LOOK_IN, CODE_EXTENSIONS, IMAGE_EXTENSIONS


class FileEngine(Base):
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
            for curr, dirs, files in os.walk(root):
                dirs[:] = self._ignore_dirs(dirs)

                for file in files:
                    if query in file.lower():
                        split_file = file.split(".")
                        is_code = split_file[-1] in CODE_EXTENSIONS
                        is_image = split_file[-1] in IMAGE_EXTENSIONS
                        file_type = (
                            "code" if is_code else "image" if is_image else "file"
                        )
                        action = "open_browser" if is_code else "open_finder"
                        path = os.path.join(curr, file)
                        if file_type == "code":
                            path = "vscode://file/" + path
                        res.append(
                            Result(
                                title=curr + "/" + file,
                                action=action,
                                action_args=path,
                                type=file_type,
                            )
                        )

                        if len(res) >= self.max_results:
                            return self._save_results(res, query)
        self._save_results(res, query)
