## Query

```sh
curl --request POST -d '{"parameters": {"top_k": 3}, "mode": "search",  "data": [{"uri":"data/1.png", "mime_type": "image/png"}]}' -H 'Content-Type: application/json' 'http://localhost:12345/search'
```
