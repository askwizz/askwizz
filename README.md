SaaS PoC by BPC

## Pitch

> Do you still know everything about your company?
> Year after year tons of information pile up and it's hard to keep track of all this knowledge.
> Not anymore.
>
> Plug, ask, get an answer.
> Using the latest AI & NLP technology, you can directly know what you need to know to run your business.

## Development

### Start milvus

```
cd milvus
docker compose up -d
```

It should start three services: milvus-standalone, milvus-minio and milvus-etcd

### Start postgres

Launch the root docker compose that has a postgres service.

```
docker-compose up -d
```

For now the env variables (password, etc...) are public.

### Start API server

Get your ip address:

```
ifconfig -u | grep 'inet ' | grep -v 127.0.0.1 | cut -d\  -f2 | head -1
```

Create `./api/.env`.

Variables needed:

```
API_OAUTH_ATLASSIAN__CLIENT_ID="" # can be empty for now
API_OAUTH_ATLASSIAN__CLIENT_SECRET=""  # can be empty for now
API_RWKV_MODEL_PATH=""  # path to a rwkv model. pth format. Download one here for example: https://huggingface.co/BlinkDL/rwkv-4-raven/blob/main/RWKV-4-Raven-1B5-v12-Eng98%25-Other2%25-20230520-ctx4096.pth
API_EMBEDDER_MODEL_NAME=""  # e5 or huggingface as of now. Pick e5 for best performance
API_SQLALCHEMY_DATABASE_URL="postgresql+psycopg2://wizz:wizzpsswd123@<your ip address>:5432/ask"  # postgres database
```

```console
cd api
poetry install
poetry run uvicorn api.app:create_app --factory
```

Server starts at http://127.0.0.1:8000

Migrate database to the latest state:

```
poe al upgrade head
```

### Start UI server

```console
cd ./ui
yarn install
yarn dev
```

Preview is available at http://localhost:3000.
