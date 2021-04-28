import os
import json

DATASET_DIR = './ShortStories'

doc_index = {}

'''
  Iterate over all documents and create a dictionary of
  doc_id against doc_name
'''
for i in range(1, 51):
  with open(os.path.join(DATASET_DIR, str(i)+'.txt')) as file:
    doc_id = file.name.split("/")
    doc_id = doc_id[-1].split(".")
    doc_id = doc_id[0]

    doc_name = file.readline().strip()

    doc_index[doc_id] = doc_name

with open('./doc_index.json', 'w') as file:
  file.write(json.dumps(doc_index))