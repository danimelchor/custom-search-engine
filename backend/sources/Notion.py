from typing import List
from custom_types import Result
from sources.Base import Base
import requests


class NotionEngine(Base):
		def __init__(self, config: dict, name: str):
				super().__init__(config, name)
				self.config = config
				self.url = config['notion']['url']
				self.token = config['notion']['api_key']
				self.headers = {
						'Authorization': 'Bearer ' + self.token,
						'Content-Type': 'application/json',
						'Notion-Version': '2022-06-28'
				}
				
		def search(self, query: str) -> List[Result]:
			payload = {
					"query": query,
					"sort": {
							"direction": "ascending",
							"timestamp": "last_edited_time"
					},
					"page_size": 100
			}
			
			response = requests.post(self.url, json=payload, headers=self.headers)
			if response.status_code == 200:
				res_json = response.json()['results'][:self.max_results]
				res = map(lambda x: Result(
					title=x['properties']['title']['title'][0]["plain_text"], 
					url=x["url"],
					source="Notion",
					type="notion"
				), res_json)
				return list(res)
			else:
				return []

