import numpy as np
import json
import string
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

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

with open("./test_queries.txt") as file:
  content = file.read()
  content = content.split("\n")

  i = 0
  while i < len(content):
    print(content[i])
    query_str = content[i].split(" ")
    query_str = pos_tag(query_str)

    i += 1

    result = content[i].split(" ")
    result = list(map(int, result))

    i += 1

    q = np.zeros((len(vocab)))
    for term, tag in query_str:
      if(len(term) >= 3):
        term = ''.join(filter(lambda x: x in printable, term))
        if(term not in stopwords):
          tag = tag[0].lower()
          if tag in ['a', 'r', 'n', 'v']:
            term = lemmatizer.lemmatize(term, tag)
          print(term)
          term_index = vocab.index(term)
          q[term_index] = idf[term]

    q /= np.linalg.norm(q)

    alpha = 0.005
    S = np.dot(D, q)

    idx = np.arange(S.size)[S > alpha]
    res = sorted(idx[np.argsort(S[idx])]+1)
    print(res)
    relevant = 0
    for doc in res:
      if doc in result:
        relevant += 1
    print("precision:",relevant/len(res), ", recall:",relevant/len(result))