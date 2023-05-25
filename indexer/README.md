# Indexer

Tool to index text documents into a vector database

## Usage

### Setup

```console
$ poetry install --only main
```

### Ingest to index

```console
$ poetry run python -m indexer.cli ingest --index-file-path db.index --text "Some context text to index"
```

or ingest from stdin (input is split by two newlines `\n\n`)

```console
$ cat texts.txt | poetry run python -m indexer.cli ingest --index-file-path db.index
```

### Search in index

```console
$ poetry run python -m indexer.cli search --index-file-path db.index "Some search prompt"
```

## Development

### Setup

```console
$ poetry install
```

