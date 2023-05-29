# Api

API exposed to the clients.

## Usage

### Setup

```console
$ poetry install --only main
```

Create and fill `.env`:

```
# Atlassian OAuth app
API_OAUTH_ATLASSIAN__CLIENT_ID=
API_OAUTH_ATLASSIAN__CLIENT_SECRET=
# path to the index file as specified in our indexer
API_INDEX=
# path to the database file
API_DATABASE=
```

### Start server

```
poetry run uvicorn api.app:create_app --factory
```

### Ingest into index

Ingestion into the index isn't exposed through the API, use the [`indexer`](../indexer) CLI to generate an index file:

```
cat tests/fixtures/texts.txt | poetry run python -m indexer.cli ingest --index-file-path tmp/test.index
```

### Search in index

```
curl localhost:8000/api/search -X POST --data '{"prompt": "What color is the sky?"}' -H "Content-Type: application/json"
```

## Development

```
poetry run uvicorn api.app:create_app --reload
```
