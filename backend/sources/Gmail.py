from typing import List
from config.SetupGoogle import get_google_creds
from sources.Base import Base
from custom_types import Result
import json

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GmailEngine(Base):
	def __init__(self, config: dict, name: str) -> None:
		super().__init__(config, name)

	def search(self, query: str, results: list) -> List[Result]:
		creds = get_google_creds()

		emails = []
		try:
				service = build('gmail', 'v1', credentials=creds)
				emails = []
				response = service.users().messages().list(
					userId='me',
					q=f"category:primary {query}"
				).execute()
				message_ids = [r['id'] for r in response.get('messages', [])][:self.max_results]
				for message_id in message_ids:
					e = service.users().messages().get(
						userId='me',
						id=message_id, 
						format="metadata"
					).execute()

					title = ""
					for header in e['payload']['headers']:
						if header['name'] == 'Subject':
							title = header['value']
							break

					e = {
						"snippet": e['snippet'],
						"title": title,
						"url": f"https://mail.google.com/mail/u/0/#inbox/{message_id}"
					}
					emails.append(e)
					
		except HttpError as error:
				print(f'An error occurred: {error}')
				emails = []

		res = map(lambda x: Result(
			title=x['title'],
			description=x['snippet'],
			action="open_browser",
			action_args=x['url'],
			type="email"
		), emails)
		results.extend(res)