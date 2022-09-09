from sources.Notion import NotionEngine
from sources.Drive import DriveEngine
from sources.Gmail import GmailEngine
from sources.Files import FileEngine

def init_sources(config: dict):
    return [
        NotionEngine(config, "notion"),
        DriveEngine(config, "drive"),
        GmailEngine(config, "gmail"),
        FileEngine(config, "files")
    ]