from typing import List
from custom_types import Result

class Base:
  def __init__(self, config: dict, name: str) -> None:
    self.config = config
    self.name = name
    self.max_results = config.get("max_results")

  def search(self, query: str, result: list) -> List[Result]:
    raise NotImplementedError

  def _save_results(self, searchResults: List[Result], resultsDict: dict) -> None:
    if searchResults:
      searchResults = searchResults[:self.max_results]
      searchResults.sort(key=lambda x: x.type)
      resultsDict[self.name] = list(map(lambda x: x.serialize(), searchResults))