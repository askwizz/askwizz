SaaS PoC by BPC

## Pitch

> Do you still know everything about your company?
> Year after year tons of information pile up and it's hard to keep track of all this knowledge.
> Not anymore.
>
> Plug, ask, get an answer.
> Using the latest AI & NLP technology, you can directly know what you need to know to run your business.

## Development

### Start the API server

Start Milvus and Postgres

```
docker compose up -d
```

Download a rwkv model from [here](https://huggingface.co/BlinkDL/rwkv-4-raven/blob/main/RWKV-4-Raven-1B5-v12-Eng98%25-Other2%25-20230520-ctx4096.pth).
Copy it to `./backend/tmp/rwkv-model.pth`.

```
mkdir backend/tmp/
wget https://huggingface.co/BlinkDL/rwkv-4-raven/resolve/main/RWKV-4-Raven-1B5-v12-Eng98%25-Other2%25-20230520-ctx4096.pth -O ./backend/tmp/
```

Create `./backend/.env`:

```
API_RWKV_MODEL_PATH="./tmp/rwkv-model.pth"
API_EMBEDDER_MODEL_NAME="e5"
API_SQLALCHEMY_DATABASE_URL="postgresql+psycopg2://postgres:password@127.0.0.1:5432/esearch"
```

Install backend Pyton environment using Poetry:

```console
cd backend
poetry install
```

Migrate database to the latest state:

```console
poetry run alembic upgrade head
```

Start server

```console
poetry run uvicorn esearch.api.app:create_app --factory
```

Server starts at http://127.0.0.1:8000.

### Start UI server

```console
cd ./ui
yarn install
yarn dev
```

Preview is available at http://localhost:3000.
