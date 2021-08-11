import pretty_errors
from jina import Flow, DocumentArray, Document
from jina.types.document.generators import from_files
from executors import ToBlobExecutor, PrintDocs
import os
import sys


flow = (
    Flow()
    # .add(uses=ToBlobExecutor, name="blobbifier") # Embed image in doc, not just filename
    .add(uses=ToBlobExecutor, name="blobbifier")
    .add(
        uses="jinahub+docker://VideoTorchEncoder",
        uses_with={"default_batch_size": 1},
        uses_metas={"workspace": "workspace"},
        name="encoder",
        volumes="./data:/encoder/data",
    )
    .add(
        uses="jinahub+docker://SimpleIndexer",
        uses_with={"index_file_name": "index"},
        uses_metas={"workspace": "workspace"},
        name="indexer",
        volumes="./workspace:/workspace/workspace",
    )
)

def index():
    if os.path.exists("workspace"):
        print("'workspace' folder exists. Please delete")
        sys.exit()

    docs = from_files('data/**/*.mp4')

    with flow:
        print("== Indexing ==")
        flow.index(inputs=docs, show_progress=True)


def query_grpc():
    query = Document(uri="data/Beethoven_1.wav")
    with flow:
        print("== Querying via gRPC ==")
        flow.search(inputs=[query], on_done=print, top_k=10)


def query_restful():
    flow.protocol = "http"
    flow.port_expose = 12345

    with flow:
        print("== Querying via REST ==")
        flow.block()


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
