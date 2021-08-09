import streamlit as st
from tempfile import NamedTemporaryFile
from config import text_endpoint, image_endpoint, images_path, top_k, image_size
import requests


def encode_to_base64(byte_string):
    import base64

    output = str(base64.b64encode(byte_string), "utf-8")

    return output


def create_query(query: str, top_k: int, endpoint: str) -> list:
    headers = {"Content-Type": "application/json"}
    data = '{"top_k":' + str(top_k) + ', "mode": "search", "data":' + query + "}"
    response = requests.post(endpoint, headers=headers, data=data)

    content = response.json()["search"]["docs"]
    results = []
    for doc in content:
        matches = doc["matches"]
        for match in matches:
            results.append(match["uri"])

    return results


def get_images(query: str, endpoint: str, top_k: int) -> dict:
    headers = {
        "Content-Type": "application/json",
    }

    data = (
        '{"parameters": {"top_k": '
        + str(top_k)
        + '}, "mode": "search",  "data": ["data:image/png;base64,'
        + query
        + '"]}'
    )

    response = requests.post(endpoint, headers=headers, data=data)
    content = response.json()
    matches = content["data"]["docs"][0]["matches"]

    return matches


def get_data(query: str, endpoint: str, top_k: int) -> dict:
    headers = {
        "Content-Type": "application/json",
    }

    data = '{"top_k":' + str(top_k) + ',"mode":"search","data":["' + query + '"]}'

    response = requests.post(endpoint, headers=headers, data=data)
    content = response.json()

    matches = content["data"]["docs"][0]["matches"]

    return matches


# layout
max_width = 1200
padding = 2


st.markdown(
    f"""
<style>
    .reportview-container .main .block-container{{
        max-width: {max_width}px;
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }}
    .reportview-container .main {{
        color: "#111";
        background-color: "#eee";
    }}
</style>
""",
    unsafe_allow_html=True,
)

# Sidebar
st.sidebar.title("Jina Image Search")

settings = st.sidebar.beta_expander(label="Settings", expanded=True)
with settings:
    endpoint = st.text_input(label="Endpoint", value=text_endpoint)
    top_k = st.number_input(label="Top K", value=top_k, step=1)

st.title("Search images by similar image")
query = st.file_uploader("Upload image")
if query is not None:
    image_data = query.read()
    query = encode_to_base64(image_data)

if st.button(label="Search"):
    if not query:
        st.markdown("Please enter a query")
    else:
        # Set up grid
        cell1, cell2, cell3 = st.beta_columns(3)
        cell4, cell5, cell6 = st.beta_columns(3)
        cell7, cell8, cell9 = st.beta_columns(3)
        all_cells = [cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell8, cell9]

        matches = get_images(query=query, endpoint=endpoint, top_k=top_k)

        for cell, match in zip(all_cells, matches):
            cell.image("http:" + match["tags"]["image_url"])
