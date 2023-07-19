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

Follow instructions in [`backend/README.md`](./backend/README.md).

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
NEXT_PUBLIC_API_HOST="127.0.0.1"
```

To get your Clerk key and secret:

- go to Clerk dashboard: https://dashboard.clerk.com/
- select the "AskWizz" organisation
- go to "API Keys"
- check that you are using the "Development" instance (top bar)
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

### Deploy using ngrok

Install ngrok

```
ngrok config add-authtoken <your token>
ngrok http 3000
```
