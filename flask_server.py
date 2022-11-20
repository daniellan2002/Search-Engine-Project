from flask import Flask, request
import time
from index import IndexManager
from BooleanQuery import boolean_search
import os
import sys

app = Flask(__name__)


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query", "")
    try:
        topk = int(request.args.get("topk", 10))
    except ValueError:
        return "Bad request: parameter \"topk\" must be a integer", 400
    start_time = time.time()
    urls = boolean_search(query, index_manager)
    search_time = round((time.time() - start_time) * 1000, 2)
    return {
        "query": query,
        "queryTime": search_time,
        "urls": urls[:topk]
    }, 200


if __name__ == "__main__":
    # https://gist.github.com/mkolod/853cda9950b898d056ac149abc45417a
    # Set hash seed and restart interpreter.
    # It is necessary if the same index file (which contain hash values of urls as doc_id) is shared on different devices.
    if not os.environ.get('PYTHONHASHSEED'):
        os.environ['PYTHONHASHSEED'] = '1234'
        os.execv(sys.executable, ['python3'] + sys.argv)

    try:
        global index_manager
        print("Initializing index... ", end="")
        index_manager = IndexManager(root="./storage")
        print("done")
        app.run(host="0.0.0.0", port=9000)
    finally:
        index_manager.close()
        print("index-related files are closed")
