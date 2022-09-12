class Result:
    def __init__(self, title: str, action: str, action_args: str, type: str, description: str = None) -> None:
        self.title = title
        self.description = description
        self.action = action
        self.action_args = action_args
        self.type = type

    def serialize(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "action": self.action,
            "action_args": self.action_args,
            "type": self.type
        }