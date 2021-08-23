from jina import Executor, requests
import os


class ProcessFile(Executor):
    @requests
    def foo(self, docs, **kwargs):
        for doc in docs:
            doc.tags["uri"] = doc.uri
            doc.tags["uri_absolute"] = os.path.abspath(doc.uri)
            doc.convert_image_uri_to_blob()
