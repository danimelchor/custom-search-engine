from typing import List
from urllib import request
from flask import Flask, request, jsonify
import yaml
from sources import init_sources
from custom_types import Result
from sources.Base import Base
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])
SOURCES: List[Base] = None

@app.route('/search', methods=['GET'])
def search():
    params = request.args
    query = params.get('q')

    results: List[Result] = []

    for source in SOURCES:
        r: Result = source.search(query)
        results.extend(r)

    serialized = [r.serialize() for r in results]
    return jsonify(serialized)

    

def start_server(host: str, port: int):
    # Load config and sources
    global SOURCES
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)
    SOURCES = init_sources(config)

    # start the server
    app.run(host=host, port=port)
