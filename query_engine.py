import numpy as np
import json
import string
import re
from pattern3.text.en import singularize

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

printable = set(string.printable)

def query(query_str):
  query_str = query_str.split(" ")
  q = np.zeros((len(vocab)))
  for term in query_str:
    term = ''.join(filter(lambda x: x in printable, term))
    if(term not in stopwords):
      term = singularize(term)
      term = re.sub(r'ly$', r'', term)
      term = re.sub(r'ed$', r'', term)
      term = re.sub(r'ing$', r'', term)
      term = re.sub(r'nes$', r'', term)
      if len(term) >= 3:
        term_index = vocab.index(term)
        q[term_index] = idf[term]

  q /= np.linalg.norm(q)

  alpha = 0.001
  S = np.dot(D, q)
  idx = np.arange(S.size)[S >= alpha]
  res = list(map(int, sorted(idx[np.argsort(S[idx])]+1)))

  return res