from typing import List
from custom_types import Result

class Base:
  def __init__(self, config: dict, name: str) -> None:
    self.config = config
    self.name = name

  def search(self, query: str) -> List[Result]:
    raise NotImplementedError