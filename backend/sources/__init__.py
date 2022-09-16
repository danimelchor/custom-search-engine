from typing import List
from sources.Notion import NotionEngine
from sources.Drive import DriveEngine
from sources.Gmail import GmailEngine
from sources.Files import FileEngine
from sources.Folders import FolderEngine
from sources.WolframAlpha import WolframAlphaEngine
from sources.Applications import ApplicationsEngine
from sources.Source import Source

SOURCES = {
    "notion": NotionEngine,
    "drive": DriveEngine,
    "gmail": GmailEngine,
    "files": FileEngine,
    "folder": FolderEngine,
    "wolframalpha": WolframAlphaEngine,
    "applications": ApplicationsEngine,
}

ENG_TO_CAT = {
    "notion": "homework and documents",
    "drive": "files and documents",
    "gmail": "emails or messages",
    "files": "files",
    "folder": "files",
    "wolframalpha": "math equation",
    "applications": "applications",
}

CATEGORIES = list(set(ENG_TO_CAT.values()))


def init_sources(
    config: dict, cat_classifications: dict, filters: list
) -> List[Source]:
    res = []
    threshold = config["acceptance_threshold"]

    for source in SOURCES:
        cat = ENG_TO_CAT[source]
        cls = SOURCES[source]
        priority = cat_classifications[cat]

        if priority > threshold or source in filters:
            res.append(cls(config, source, priority))

    return res
