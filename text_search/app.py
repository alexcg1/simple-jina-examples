import sys
import os
from jina import Flow, Document
from jina.types.document.generators import from_csv


flow = (
    Flow()
    .add(
        name="encoder",
        uses="jinahub+docker://TransformerTorchEncoder",
    )
    .add(
        name="indexer",
        uses="jinahub+docker://SimpleIndexer",
        uses_with={"index_file_name": "index"},
        uses_metas={"workspace": "workspace"},
        volumes="./workspace:/workspace/workspace",
    )
)

# Start the Flow
def index():
    if os.path.exists("workspace"):
        print("'workspace' folder exists. Please delete")
        sys.exit()

    data_file = "data/community_20.csv"
    # Open our data CSV
    with open(data_file) as file:
        # Create a DocumentArray from the CSV, choosing "title" as the field to encode and index
        docs = list(from_csv(file, field_resolver={"title": "text"}))

    with flow:
        flow.post(on="/index", inputs=docs)  # Set the Flow to index


def query_restful():
    flow.protocol = "http"
    flow.port_expose = 12345
    with flow:
        flow.block()  # Keep the Flow open, ready for user to search


def query_grpc():
    with flow:
        print("== Querying via gRPC ==")
        flow.search(inputs=[Document(text="hello world")], on_done=print, top_k=10)


if len(sys.argv) < 1:
    print("Supported arguments: index, query_restful, query_grpc")
if sys.argv[1] == "index":
    index()
elif sys.argv[1] == "query_restful":
    query_restful()
elif sys.argv[1] == "query_grpc":
    query_grpc()
else:
    print("Supported arguments: index, query_restful, query_grpc")
