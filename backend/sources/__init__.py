from sources.Notion import NotionEngine
from sources.Drive import DriveEngine
from sources.Gmail import GmailEngine
from sources.Files import FileEngine
from sources.Folders import FolderEngine
from sources.WolframAlpha import WolframAlphaEngine
from sources.Applications import ApplicationsEngine


def init_sources(config: dict):
    return [
        NotionEngine(config, "notion"),
        DriveEngine(config, "drive"),
        GmailEngine(config, "gmail"),
        FileEngine(config, "files"),
        FolderEngine(config, "folder"),
        WolframAlphaEngine(config, "wolframalpha"),
        ApplicationsEngine(config, "applications"),
    ]
