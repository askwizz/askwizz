# Generic single-database configuration.

## Create a new migration file

```bash
poetry run alembic revision -m "<Migration name>"
poetry run alembic revision -m "Create connection table"
```

## Apply migrations

```bash
poetry run alembic upgrade head
```
