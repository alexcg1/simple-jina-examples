from jina import Executor, requests


class ToBlobExecutor(Executor):
    @requests
    def foo(self, docs, **kwargs):
        for doc in docs:
            doc.convert_image_uri_to_blob()
