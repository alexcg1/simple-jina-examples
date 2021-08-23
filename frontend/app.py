import streamlit as st
from config import image_endpoint, top_k
from helper import search_by_file, UI

endpoint = image_endpoint
text_endpoint = image_endpoint


st.markdown(
    body=UI.css,
    unsafe_allow_html=True,
)

# Sidebar
st.sidebar.title("Jina Simple Frontend")

media_type = st.sidebar.radio(
    label="Media type", options=["Text", "Image", "Audio", "Video"], index=1
)

settings = st.sidebar.expander(label="Settings", expanded=True)
with settings:
    endpoint = st.text_input(label="Endpoint", value=text_endpoint)
    top_k = st.number_input(label="Top K", value=top_k, step=1)

# Main area
if media_type == "Image":
    st.title("Search images by similar image")

if media_type != "Text":
    query = st.file_uploader("Upload file")
else:
    query = st.text_input("Search phrase")

if st.button(label="Search"):
    if not query:
        st.markdown("Please enter a query")
    else:
        matches = search_by_file(query, top_k)

        # Set up grid
        cell1, cell2, cell3 = st.columns(3)
        cell4, cell5, cell6 = st.columns(3)
        cell7, cell8, cell9 = st.columns(3)
        all_cells = [cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell8, cell9]

        for cell, match in zip(all_cells, matches):
            cell.image(match["tags"]["uri_absolute"], width=128)
