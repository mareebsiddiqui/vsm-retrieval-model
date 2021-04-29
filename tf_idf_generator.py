import os
import re
import json
import string
from pattern3.text.en import singularize
import numpy as np

DATASET_DIR = './ShortStories'
STOPWORDS_FILE = './Stopword-List.txt'

'''
  Fetches all the stopwords in a global stopwords array
'''
stopwords = []
with open(STOPWORDS_FILE) as file:
  stopwords = file.read()
  stopwords = stopwords.split("\n")
  stopwords = [stopword for stopword in stopwords if stopword]

printable = set(string.printable)
doc_tf = {}
idf = {}

for i in range(1, 51):
  with open(os.path.join(DATASET_DIR, str(i)+'.txt')) as file:
    words = file.read()
    words = re.sub(r'\n|--', r' ', words)
    words = re.sub(r'“|”|’|‘|;|,|!|:|\.|\?|\)|\(|\*', r'', words)
    words = words.lower()
    words = re.split(r" |-|\u2014", words)
    words = [word for word in words if word]
    
    for word in words:
      word = ''.join(filter(lambda x: x in printable, word))
      if(word not in stopwords):
        word = singularize(word)
        word = re.sub(r'ly$', r'', word)
        word = re.sub(r'ed$', r'', word)
        word = re.sub(r'ing$', r'', word)
        word = re.sub(r'nes$', r'', word)
        if len(word) >= 3:
          if (i, word) not in doc_tf:
            doc_tf[i, word] = 1

            if word not in idf:
                idf[word] = 1
            else:
                idf[word] += 1
          else:
            doc_tf[i, word] += 1

for term, freq in idf.items():
  idf[term] = np.log10(50/(freq+1))

vocab = [x for x in idf]
print(len(vocab))
D = np.zeros((50, len(vocab)))
for doc_id, doc in enumerate(doc_tf):
    doc_id = doc[0]-1
    term_index = vocab.index(doc[1])
    D[doc_id][term_index] = doc_tf[doc]*idf[doc[1]]

row_sums = np.linalg.norm(D, axis=1)
D /= row_sums[:, np.newaxis]

np.save('document_vectors.npy', D)

with open("./vocab.json", 'w') as file:
  file.write(json.dumps(vocab))

with open("./idfs.json", 'w') as file:
  file.write(json.dumps(idf))