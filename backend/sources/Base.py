from typing import List
from custom_types import Result

class Base:
  def __init__(self, config: dict) -> None:
    self.config = config

  def search(self, query: str) -> List[Result]:
    raise NotImplementedError