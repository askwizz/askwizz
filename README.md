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
docker-compose up -d milvus db
# On darwin
COMPOSE_DOCKER_CLI_BUILD=1 DOCKECOMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 DOCKER_DEFAULT_PLATFORM=linux/amd64 docker-compose up --build
```

Download a rwkv model from [here](https://huggingface.co/BlinkDL/rwkv-4-raven/blob/main/RWKV-4-Raven-1B5-v12-Eng98%25-Other2%25-20230520-ctx4096.pth).
Copy it to `./backend/tmp/rwkv-model.pth`.

```
mkdir backend/tmp/
wget https://huggingface.co/BlinkDL/rwkv-4-raven/resolve/main/RWKV-4-Raven-1B5-v12-Eng98%25-Other2%25-20230520-ctx4096.pth -O ./backend/tmp/rwkv-model.pth
```

Create `./backend/.env`:

```
API_RWKV_MODEL_PATH="./tmp/rwkv-model.pth"
API_EMBEDDER_MODEL_NAME="e5"
API_SQLALCHEMY_DATABASE_URL="postgresql+psycopg2://postgres:password@127.0.0.1:5432/esearch"
API_OAUTH_ATLASSIAN__CLIENT_ID=""
API_OAUTH_ATLASSIAN__CLIENT_SECRET=""
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
poetry run uvicorn esearch.api.app:create_app --reload
```

Server starts at http://127.0.0.1:8000.

### Start UI server

Create `./ui/.env.development.local`, fill with your key from Clerk Dashboard:

```
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/
NEXT_PUBLIC_DEBUG=true
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=<your_key>
CLERK_SECRET_KEY=<your_secret>
API_HOST="127.0.0.1"
```

To get your Clerk key and secret:

- go to Clerk dashboard: https://dashboard.clerk.com/
- select the "AskWizz" organisation
- go to "API Keys"
- copy the content from the `.env.local` box.

Start server

```console
cd ./ui
yarn install
yarn dev
```

Preview is available at http://localhost:3000.

## Deployment

### Start the services

```
docker-compose up
# Connect to api to run migrations
docker exec -it api bash
poetry run alembic upgrade head
```
