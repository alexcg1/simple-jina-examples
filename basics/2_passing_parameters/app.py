# This example follows "minimum_example".
# In this example we do the following:
# 1. Move some things to helper.py to keep app.py light
# 2. Use "uses_with", "uses_metas", and "volumes" to pass more parameters to our Executors

from jina import Document, Flow
from helper import docs, print_search_results

flow = (
    Flow()
    .add(
        uses="jinahub+docker://SpacyTextEncoder",
        uses_with={"model_name": "en_core_web_md"},
        name="encoder",
    )
    .add(
        uses="jinahub+docker://SimpleIndexer",
        uses_metas={"workspace": "workspace"},
        volumes="./workspace:/workspace/workspace",
        name="indexer",
    )
)

with flow:
    flow.index(inputs=docs)
    query = Document(text=input("Please enter your search term: "))
    response = flow.search(inputs=query, return_results=True)

print_search_results(response)
