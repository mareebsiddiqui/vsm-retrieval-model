from flask import Flask, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

import query_engine

'''
    Receives: query: string
    Returns: {
        results: documents,
        search_words: words that matched in the document
    }
'''
@app.route('/query')
def get_query_results():
    query = request.args.get('query')
    query = query_engine.query(query)
    print(query)
    return {
        "results": query
    }

'''
    Receives: doc_id
    Returns: {
        doc_name,
        doc
    }
'''
@app.route('/document')
def get_document():
    doc_id = request.args.get('doc_id')
    doc = None
    with open('./ShortStories/{doc_id}.txt'.format(doc_id = doc_id)) as f:
        doc_name = f.readline().strip()
        doc = f.read()

    return {
        "doc_name": doc_name,
        "doc": doc
    }

'''
    Receives: -
    Returns: index of document ids against document names
'''
@app.route('/doc_index')
def get_doc_index():
    doc_index = {}
    with open('./doc_index.json', 'r') as file:
        doc_index = json.load(file)

    return doc_index

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, lazy_loading=True)