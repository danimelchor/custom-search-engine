from typing import List
from custom_types import Result
import json


class Base:
    def __init__(self, config: dict, name: str, priority: int) -> None:
        self.config = config
        self.name = name
        self.max_results = config.get("max_results")
        self.max_description_length = config.get("max_description_length")
        self.priority = priority

    async def search(self, query: str) -> None:
        try:
            res = await self._search(query)
            self._save_results(res, query)
        except Exception as e:
            print(f"Error in {self.name}: {e}")

    async def _search(self, query: str) -> List[Result]:
        raise NotImplementedError

    def _save_results(self, search_results: List[Result], query: str) -> None:
        if search_results:
            search_results = search_results[: self.max_results]
            search_results.sort(key=lambda x: x.type)

            serialized_res = []
            for res in search_results:
                serialized_res.append(res.serialize(self.max_description_length))

            result = {
                "priority": self.priority,
                "name": self.name,
                "results": serialized_res,
                "query": query,
            }

            result_json = json.dumps(result)
            print(result_json)
