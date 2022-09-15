class Result:
    def __init__(
        self,
        title: str,
        action: str,
        action_args: str,
        type: str,
        description: str = "",
    ) -> None:
        self.title = title
        self.description = description
        self.action = action
        self.action_args = action_args
        self.type = type

    def serialize(self, max_description_length) -> dict:
        return {
            "title": self.title,
            "description": self.description[:max_description_length],
            "action": self.action,
            "action_args": self.action_args,
            "type": self.type,
        }
