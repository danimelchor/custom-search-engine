import threading
from typing import Dict, List
from urllib import request
from flask import Flask, request, jsonify
import yaml
from sources import init_sources
from custom_types import Result
from sources.Base import Base
from flask_cors import CORS
from utils import run_in_thread

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])
SOURCES: List[Base] = None

@app.route('/search', methods=['GET'])
def search():
    params = request.args
    query = params.get('q')

    sources = [s.strip().split(":")[1] for s in query.split(" ") if s.startswith("in:")]
    query = " ".join([s for s in query.split(" ") if not s.startswith("in:")])

    if not query:
        return jsonify([])

    results: Dict[str, dict] = {}
    threads: List[threading.Thread] = []
    for source in SOURCES:
        if not sources or source.name in sources:
            thread = run_in_thread(source.search, query=query, results=results)
            threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    return jsonify(results)

    

def start_server(host: str, port: int):
    # Load config and sources
    global SOURCES
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)
    SOURCES = init_sources(config)

    # start the server
    app.run(host=host, port=port)
