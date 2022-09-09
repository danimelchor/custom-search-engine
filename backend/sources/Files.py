from typing import List
from sources.Base import Base
from custom_types import Result
import os, re

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
CODE_EXTENSIONS = set([
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
])

# Files considered images
IMAGE_EXTENSIONS = set([
  "png",
  "jpg",
  "jpeg",
  "gif",
  "svg",
  "bmp",
])

class FileEngine(Base):
  def __init__(self, config: dict, name: str) -> None:
    super().__init__(config, name)

  def _ignore_dirs(self, dirs: list) -> list:
    return list(filter(lambda d: self._should_use(d), dirs))

  def _should_use(self, name: str) -> bool:
    return re.match(IGNORED_PATTERNS, name) is None

  def search(self, query: str, results: list) -> List[Result]:
    res = []
    for root in roots_to_look_in:
      for curr, dirs, files in os.walk(root):
        dirs[:] = self._ignore_dirs(dirs)

        for file in files:
            if query in file and self._should_use(file):
                url = f"vscode://file/{os.path.join(curr, file)}"
                is_code = file.split(".")[-1] in CODE_EXTENSIONS
                is_image = file.split(".")[-1] in IMAGE_EXTENSIONS
                type = "code" if is_code else "image" if is_image else "file"
                res.append(
                  Result(
                    title=curr + "/" + file,
                    url=url,
                    type=type,
                    source="Files"
                  )
                )
    results.extend(res[:self.max_results])