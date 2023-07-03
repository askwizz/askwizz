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

Follow instructions in [`./backend`](./backend/README.md).

### Start UI server

Follow instructions in [`./ui`](./ui/README.md).

## Deployment

Follow instructions in [`./backend`](./backend/README.md) to download the model.

```console
$ docker-compose up
```

Connect to api to run migrations

```console
$ docker exec -it api bash
# poetry run alembic upgrade head
```
