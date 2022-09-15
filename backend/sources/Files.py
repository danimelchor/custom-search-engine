from typing import List
from sources.Base import Base
from custom_types import Result
import os, re, asyncio

# Regex patterns to ignore
ignored_patterns_list = [
    r"^node_modules$",
    r"^venv$",
    r"^env$",
    r"^\..*",
    r"^_.*",
    r"^obj$",
    r"^bin$",
    r"^build$",
    r"^cache$",
    r"^dist$",
    r"^temp$",
    r"^tmp$",
    r".*undo.*",
]

# Combine the regex patterns into one
IGNORED_PATTERNS = "(" + ")|(".join(ignored_patterns_list) + ")"

# Root directories to look in
roots_to_look_in = [
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/Documents"),
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Pictures"),
    os.path.expanduser("~/Music"),
    os.path.expanduser("~/Movies"),
    os.path.expanduser("~/Applications"),
]

# Files considered code
CODE_EXTENSIONS = set(
    [
        "py",
        "cpp",
        "c",
        "js",
        "ts",
        "html",
        "css",
        "scss",
        "sass",
        "less",
        "json",
        "md",
        "txt",
        "sh",
        "yaml",
        "yml",
        "xml",
        "java",
        "kt",
        "go",
        "rs",
        "rb",
        "php",
        "swift",
        "dart",
        "h",
    ]
)

# Files considered images
IMAGE_EXTENSIONS = set(
    [
        "png",
        "jpg",
        "jpeg",
        "gif",
        "svg",
        "bmp",
    ]
)


class FileEngine(Base):
    def __init__(self, config: dict, name: str) -> None:
        super().__init__(config, name)

    def _ignore_dirs(self, dirs: list) -> list:
        return list(filter(lambda d: self._should_use(d), dirs))

    def _should_use(self, name: str) -> bool:
        return re.match(IGNORED_PATTERNS, name, re.IGNORECASE) is None

    async def search(self, query: str, results: list) -> None:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.sync_search, query, results)

    def sync_search(self, query: str, results: list) -> None:
        res = []
        for root in roots_to_look_in:
            for curr, dirs, files in os.walk(root):
                dirs[:] = self._ignore_dirs(dirs)

                for dir in dirs:
                    if query in dir and self._should_use(dir):
                        res.append(
                            Result(
                                title=os.path.join(curr, dir) + "/",
                                action="open_finder",
                                action_args=os.path.join(curr, dir),
                                type="dir",
                            )
                        )

                        if len(res) >= self.max_results:
                            return self._save_results(res, results)

                for file in files:
                    if query in file.lower() and self._should_use(file):
                        is_code = file.split(".")[-1] in CODE_EXTENSIONS
                        is_image = file.split(".")[-1] in IMAGE_EXTENSIONS
                        type = "code" if is_code else "image" if is_image else "file"
                        path = os.path.join(curr, file)
                        if type == "code":
                            path = "vscode://file/" + path
                        res.append(
                            Result(
                                title=curr + "/" + file,
                                action="open_finder"
                                if type != "code"
                                else "open_browser",
                                action_args=path,
                                type=type,
                            )
                        )

                        if len(res) >= self.max_results:
                            return self._save_results(res, results)
        self._save_results(res, results)
