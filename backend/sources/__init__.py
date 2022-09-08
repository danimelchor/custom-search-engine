from sources.Notion import NotionEngine
from sources.Drive import DriveEngine
from sources.Gmail import GmailEngine

def init_sources(config: dict):
    return [
        NotionEngine(config),
        DriveEngine(config),
        GmailEngine(config)
    ]