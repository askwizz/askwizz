SaaS PoC by BPC

## Pitch

> Do you still know everything about your company?
> Year after year tons of information pile up and it's hard to keep track of all this knowledge.
> Not anymore.
>
> Plug, ask, get an answer.
> Using the latest AI & NLP technology, you can directly know what you need to know to run your business.

## Development

Start API server

Note: you need to create `./api/.env`.

```console
cd ./api
poetry install
poetry run uvicorn api.app:create_app --reload
```

Start UI server

```console
cd ./ui
yarn install
yarn dev
```

Preview is available at http://localhost:5173.
