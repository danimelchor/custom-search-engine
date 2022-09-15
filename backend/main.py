from re import A
from typing import Dict, List
import yaml
from sources import init_sources
from sources.Base import Base
from utils import parse_args
import os
import json
import asyncio

async def search(query: str, sources: List[Base]) -> None:
    filters = [s.strip().split(":")[1] for s in query.split(" ") if s.startswith("in:")]
    query = " ".join([s for s in query.split(" ") if not s.startswith("in:")])

    if not query:
        return
    
    results: Dict[str, dict] = {}
    tasks: List[asyncio.Task] = []
    for source in sources:
        if not filters or source.name in filters:
            task = source.search(query, results)
            tasks.append(task)


    # Wait for all tasks to finish
    await asyncio.gather(*tasks)

    # Sort results by priority
    sorted_keys = sorted(results.keys(), key=lambda x: x[0], reverse=True)
    results = { k[1]: results[k] for k in sorted_keys}

    # Print results
    json_res = json.dumps(results)
    print(json_res)

def load_config():
    current_abs_path = os.path.abspath(__file__)
    absolute_config = os.path.join(os.path.dirname(current_abs_path), "./config/config.yaml")
    
    with open(absolute_config, "r") as f:
        return yaml.safe_load(f)

if __name__ == "__main__":
    query = parse_args()
    config = load_config()
    sources = init_sources(config)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(search(query, sources))
