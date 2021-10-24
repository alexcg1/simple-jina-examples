from jina import Document, DocumentArray, Flow

docs = DocumentArray(
    [
        Document(text="I’m Good At Everything, Except The Things I Can’t Do."),
        Document(
            text="I Don’t Have A Home To Go Back To. In Here, I Stand A Chance At Least. But Out There? I Got Nothing Out There."
        ),
        Document(text="This Is Hell. What Are The Rules In Hell?"),
        Document(
            text="Do You Know What Someone With No Money Has In Common With Someone With Too Much Money? Living Is No Fun For Them."
        ),
        Document(
            text="You Don’t Trust People Here Because You Can. You Do It Because You Don’t Have Anybody Else."
        ),
    ]
)

flow = (
    Flow()
    .add(uses="jinahub+docker://SpacyTextEncoder", name="encoder")
    .add(uses="jinahub://SimpleIndexer", install_requirements=True, name="indexer")
)

with flow:
    flow.index(inputs=docs)
    query = Document(text=input("Please enter your search term: "))
    response = flow.search(inputs=query, return_results=True)

matches = response[0].data.docs[0].matches

print("Your search results")
print("-------------------\n")

for match in matches:
    print(f"- {match.text}")
