class Result:
    def __init__(self, source: str, title: str, url: str, type: str, description: str = None) -> None:
        self.source = source
        self.title = title
        self.description = description
        self.url = url
        self.type = type

    def serialize(self) -> dict:
        return {
            "source": self.source,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "type": self.type
        }