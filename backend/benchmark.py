import asyncio
from collections import defaultdict
from typing import List
from sources import init_sources
from sources.Source import Source
from main import load_config
import time


async def search(query: str, sources: List[Source]) -> dict:
    results = defaultdict(list)
    for source in sources:
        now = time.time()
        await source.search(query, results)
        took = time.time() - now
        res = [v for k, v in results.items() if k[1] == source.name] or [[]]

        result_text = ",".join(map(lambda x: x["title"], res[0]))
        print(f"{source.name}: {took}s, {len(res[0])} results, ({result_text})")


if __name__ == "__main__":
    config = load_config()
    sources = init_sources(config)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(search("brave", sources))
