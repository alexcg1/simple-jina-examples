# In this example we do the following:
# 1. Change to a more "real-world" csv
# 2. Extract text and metadata from the csv

from jina import Document, DocumentArray, Flow
from jina.types.document.generators import from_csv
from helper import print_search_results

with open("data/anime.csv") as file:
    docs = DocumentArray(from_csv(file, field_resolver={"Description": "text"}))

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
