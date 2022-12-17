from flask import Flask, request, render_template
# from flask_cors import CORS, cross_origin
import time
from index import IndexManager
from BooleanQuery import boolean_search
from CosineSimilarity import cosineScore
from utils import set_hash_seed
import os
import sys

app = Flask(__name__, template_folder="WebUI/template", static_folder="WebUI/static")
# cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/search", methods=["GET"])
# @cross_origin()
def search():
    query = request.args.get("query", "")
    try:
        perPage = int(request.args.get("perPage", 10))
        page = int(request.args.get("page", 1))
        if page < 1:
            return f"Bad request: parameter \"page\" must be 1 or greater, {page} is given", 400
        if perPage < 1:
            return f"Bad request: parameter \"perPage\" must be 1 or greater, {perPage} is given", 400
    except ValueError:
        return "Bad request: parameter \"perPage\" and \"page\" must be a integer", 400
    start_time = time.time()
    # urls = boolean_search(query, index_manager)
    urls = cosineScore(query, index_manager)
    search_time = round((time.time() - start_time) * 1000, 2)
    return {
        "query": query,
        "queryTime": search_time,
        "urls": urls[perPage * (page - 1):perPage * page] if perPage * (page - 1) < len(urls) else [],
        "resultNum": len(urls)
    }, 200


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/ranking.html", methods=["GET"])
def ranking():
    return render_template("ranking.html")


if __name__ == "__main__":
    set_hash_seed()

    try:
        global index_manager
        print("Initializing index... ", end="")
        index_manager = IndexManager(55393, root="./storage")
        print("done")
        app.run(host="0.0.0.0", port=9000)
    finally:
        index_manager.close()
        print("index-related files are closed")
