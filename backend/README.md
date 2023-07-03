# Api

API exposed to the clients.

## Development

Start Milvus and Postgres from the top-level folder of the repo.

```console
$ docker-compose up -d milvus db
```

if you are on `darwin` (MacOS), use this command instead:

```console
$ COMPOSE_DOCKER_CLI_BUILD=1 DOCKECOMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 DOCKER_DEFAULT_PLATFORM=linux/amd64 docker-compose up --build
```

Now, in this folder.

Download a rwkv model from [here](https://huggingface.co/BlinkDL/rwkv-4-raven/blob/main/RWKV-4-Raven-1B5-v12-Eng98%25-Other2%25-20230520-ctx4096.pth).
Copy it to `./tmp/rwkv-model.pth`.

```console
$ mkdir tmp/
$ wget https://huggingface.co/BlinkDL/rwkv-4-raven/resolve/main/RWKV-4-Raven-1B5-v12-Eng98%25-Other2%25-20230520-ctx4096.pth -O ./tmp/rwkv-model.pth
```

Create `.env`:

```
API_RWKV_MODEL_PATH="./tmp/rwkv-model.pth"
API_EMBEDDER_MODEL_NAME="e5"
API_SQLALCHEMY_DATABASE_URL="postgresql+psycopg2://postgres:password@127.0.0.1:5432/esearch"
API_OAUTH_ATLASSIAN__CLIENT_ID=""
API_OAUTH_ATLASSIAN__CLIENT_SECRET=""
```

Install backend Pyton environment using Poetry:

```console
$ poetry install
```

Migrate database to the latest state:

```console
$ poetry run alembic upgrade head
```

Create a connection (get a token following [this](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/).

```console
$ poetry run python -m esearch.cli ingest_connection --domain bpc-ai.atlassian.net --email <your-email> --token <your-token>
```

Start server

```console
$ poetry run uvicorn esearch.api.app:create_app --reload
```

Server starts at http://127.0.0.1:8000.

