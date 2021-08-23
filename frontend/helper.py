import magic
import requests
from config import image_endpoint, images_path, image_size
from tempfile import NamedTemporaryFile

headers = {"Content-Type": "application/json"}

class UI:
    css = f"""
<style>
    .reportview-container .main .block-container{{
        max-width: 1200px;
        padding: 2rem;
    }}
    .reportview-container .main {{
        color: "#111";
        background-color: "#eee";
    }}
</style>
"""


def search_by_file(query, top_k, endpoint):
    data = query.read()
    tempfile = NamedTemporaryFile()

    with open(tempfile.name, "wb") as file:
        file.write(data)

    filetype = magic.from_file(tempfile.name, mime=True)

    data = (
        '{"parameters": {"top_k": '
        + str(top_k)
        + '}, "mode": "search",  "data": [{"uri": "'
        + tempfile.name
        + '", "mime_type": "'
        + filetype
        + '"}]}'
    )

    response = requests.post(endpoint, headers=headers, data=data)
    content = response.json()
    matches = content["data"]["docs"][0]["matches"]

    return matches
