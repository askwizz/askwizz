# Api

API exposed to the clients.

## Development

Start Milvus and Postgres from the top-level folder of the repo.

```
docker-compose up -d milvus db
# On darwin
COMPOSE_DOCKER_CLI_BUILD=1 DOCKECOMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 DOCKER_DEFAULT_PLATFORM=linux/amd64 docker-compose up --build
```

Now, in this folder.

Download a rwkv model from [here](https://huggingface.co/BlinkDL/rwkv-4-raven/blob/main/RWKV-4-Raven-1B5-v12-Eng98%25-Other2%25-20230520-ctx4096.pth).
Copy it to `./tmp/rwkv-model.pth`.

```
mkdir tmp/
wget https://huggingface.co/BlinkDL/rwkv-4-raven/resolve/main/RWKV-4-Raven-1B5-v12-Eng98%25-Other2%25-20230520-ctx4096.pth -O ./tmp/rwkv-model.pth
```

Create `.env`:

```
API_RWKV_MODEL_PATH="./tmp/rwkv-model.pth"
API_EMBEDDER_MODEL_NAME="e5"
API_SQLALCHEMY_DATABASE_URL="postgresql+psycopg2://postgres:password@127.0.0.1:5432/esearch"
API_OAUTH_ATLASSIAN__CLIENT_ID=""
API_OAUTH_ATLASSIAN__CLIENT_SECRET=""
```

Install backend Python environment using Poetry:

```console
poetry install
```

Migrate database to the latest state:

```console
poetry run alembic upgrade head
```

Create a connection (get a token following [this](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/).

```console
poetry run python -m esearch.cli ingest_connection --domain bpc-ai.atlassian.net --email <your-email> --token <your-token>
```

Start server

```console
poetry run uvicorn esearch.api.app:create_app --reload --log-level debug
```

Server starts at http://127.0.0.1:8000.

## Tests

```bash
poetry run pytest .
```

Generate snapshots

```bash
poetry run pytest --snapshot-update .
```

Formatter

```bash
poetry run black .
```

Ruff

```bash
poetry run ruff .
```

## Calling the API

```
curl -X POST http://127.0.0.1:8000/api/search \
  -d '{ "query": "What is a bad bank ?" }' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer xxxxxx'
```

```
curl http://127.0.0.1:8000/api/history/search \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer xxxxxx'
```

```
curl -X POST http://127.0.0.1:8000/api/passage/text \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer xxxxxx' \
  -d '{ "connection_id": "353cad4f-5476-4581-801e-bf7e89d0d533", "config": { "confluence": { "passage_hash": "6268a86c229bec218a9b0ffc261e359e", "page_path": "/spaces/TW/pages/688378/Bad+bank" } } }'
```

## Entity Architecture

**connection**

- a user_id (clerk id)
- connection_type: str
- connection_data: json. Object with info for establishing the connection
- name
- status: "indexing" | ""

**query**

- user_id
- text: str (="What is a toto ?" | "What is toto?created_at<=2021.01.01&connection=xueyfgezigu") (or json field with semi striuctured query search)
- created_at

```mermaid
erDiagram





```

Tracking user actions

https://amplitude.com/pricing
