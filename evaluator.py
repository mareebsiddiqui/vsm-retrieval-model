import numpy as np
import json
import string
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

import query_engine

STOPWORDS_FILE = './Stopword-List.txt'

D = np.load('document_vectors.npy')

vocab = None
with open("./vocab.json") as f:
  vocab = json.load(f)

idf = None
with open("./idfs.json") as f:
  idf = json.load(f)

stopwords = []
with open(STOPWORDS_FILE) as file:
  stopwords = file.read()
  stopwords = stopwords.split("\n")
  stopwords = [stopword for stopword in stopwords if stopword]

lemmatizer = WordNetLemmatizer()

printable = set(string.printable)

ps = []
rs = []

with open("./test_queries.txt") as file:
  content = file.read()
  content = content.split("\n")

  i = 0
  while i < len(content):
    print(content[i])
    res = query_engine.query(content[i])
    
    i += 1

    result = content[i].split(" ")
    result = list(map(int, result))
    
    i += 1

    print(res)
    print(len(res))
    relevant = 0
    for doc in res:
      if doc in result:
        relevant += 1

    ps.append(relevant/len(res))
    rs.append(relevant/len(result))

    print("precision:",relevant/len(res), ", recall:",relevant/len(result))

print(sum(ps)/len(ps))
print(sum(rs)/len(rs))