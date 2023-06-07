# Api

API exposed to the clients.

## Usage

### Setup

```console
$ poetry install --only main
```

Create and fill `.env`:

```bash
# Atlassian OAuth app
API_OAUTH_ATLASSIAN__CLIENT_ID=
API_OAUTH_ATLASSIAN__CLIENT_SECRET=

# path to rwkv llm model
API_RWKV_MODEL_PATH=
# embedder model name (e5 or huggingface supported)
API_EMBEDDER_MODEL_NAME=
```

### Start server

```
poetry run uvicorn api.app:create_app --factory
```

### Authentication: get clerk token (todo)

### Ingest into index

```
curl localhost:8000/api/index -X POST \
          --data '{ "atlassian_email": "maximeduvalsy@gmail.com", "atlassian_token": <token>, "space_key": "TW", "wiki_url": "https://bpc-ai.atlassian.net/wiki" }' \
          -H "Content-Type: application/json"
```

### Search in index

```
curl localhost:8000/api/search -X POST --data '{"query": "Swedish banking crisis", "connection_name": "newconnection"}' -H "Content-Type: application/json"
  -H "Authorization: Bearer <clerk token>"
```

### Add connection

```
curl localhost:8000/api/new-connection -X POST \
  --data '{"name": "My connection", "email": "maximeduvalsy@gmail.com", "token": <atlassian token>}' \
  -H "Authorization: Bearer <clerk token>"
```

## Development

```
poetry run uvicorn api.app:create_app --reload
```
