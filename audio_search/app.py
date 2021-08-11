import pretty_errors
from jina import Flow, DocumentArray, Document
from jina.types.document.generators import from_files
from executors import ToBlobExecutor, PrintDocs
import os
import sys


flow = (
    Flow()
    # .add(uses=ToBlobExecutor, name="blobbifier") # Embed image in doc, not just filename
    .add(
        uses="jinahub+docker://VGGishAudioEncoder",
        # uses_with={"model_name": "R50x1", "model_path": "model"},
        uses_metas={"workspace": "workspace"},
        name="encoder",
        volumes="./data:/encoder/data",
    )
    .add(uses="PrintDocs", name="printer")
    .add(
        uses="jinahub+docker://SimpleIndexer",
        uses_with={"index_file_name": "index"},
        uses_metas={"workspace": "workspace"},
        name="indexer",
        volumes="./workspace:/workspace/workspace",
    )
    .add(uses="PrintDocs", name="printer")
)


def index():
    if os.path.exists("workspace"):
        print("'workspace' folder exists. Please delete")
        sys.exit()

    NUM_DOCS = 3  # Keeping this low for fast testing
    docs = DocumentArray(from_files("data/**/*.mp3"))[:NUM_DOCS]  # Limit number for now

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
