import pretty_errors
from jina import Flow, DocumentArray, Document, Executor, requests
from jina.types.document.generators import from_files
import os
import sys

docs = DocumentArray(from_files("data/**/*.png"))[:10]  # Limit number for now
query_image = Document(uri="./data/1.png")

for doc in docs:
    doc.convert_image_uri_to_blob()

query_image.convert_image_uri_to_blob()

flow = (
    Flow(protocol="http", port_expose=12345)
    .add(
        uses="jinahub+docker://ImageNormalizer",
        name="crafter",
        override_with={"target_size": 40},
    )
    .add(
        uses="jinahub+docker://BigTransferEncoder",
        override_with={"model_name": "R50x1", "model_path": "model"},
        override_metas={"workspace": "workspace"},
        name="encoder",
        volumes="./data:/encoder/data",
    )
    .add(
        uses="jinahub+docker://SimpleIndexer",
        override_with={"index_file_name": "index"},
        override_metas={"workspace": "workspace"},
        name="indexer",
        volumes="./workspace:/workspace/workspace",
    )
)


def index(inputs):
    with flow:
        print("== Indexing ==")
        flow.index(inputs=inputs, show_progress=True)


def query_grpc(query_image):
    with flow:
        print("== Querying via gRPC ==")
        flow.search(inputs=[query_image], on_done=print, top_k=1)
        flow.block()


def query_restful():
    with flow:
        print("== Querying ==")
        flow.block()


index(docs)
query_restful()
