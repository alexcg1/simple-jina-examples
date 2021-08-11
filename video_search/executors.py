from jina import Executor, requests
from torchvision.io.video import read_video


class ToBlobExecutor(Executor):
    @requests
    def blobify(self, docs, **kwargs):
        for doc in docs:
            video_array, _, _ = read_video(doc.uri)  # video frames in the shape of `NumFrames x Height x Width x 3`
            video_array = video_array.cpu().detach().numpy()
            doc.blob = video_array

class PrintDocs(Executor):
    @requests
    def print_docs(self, docs, **kwargs):
        print(docs)
