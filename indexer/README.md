# Indexer

Tool to index text documents into a vector database

```
poetry install
```

Generate the index

```
poetry run python src/create_index.py
```

Find the most similar documents to a given query

```
poetry run python src/find_in_index.py
```

## TODO

Results are bad right now.
Need to improve understanding of retriever:

- Maybe the texts are too big ?
- Maybe the retriever model is not the right one ?
- Maybe this semantic search paradigm is not the right one ?

Read:

- https://hackernoon.com/a-practical-5-step-guide-to-do-semantic-search-on-your-private-data-with-the-help-of-llms
- https://dylancastillo.co/semantic-search-elasticsearch-openai-langchain/
