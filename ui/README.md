# UI

Web UI (client) to the AskWizz service.

## Development

Create `./ui/.env.development.local`, fill with your key from Clerk Dashboard:

```
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/
NEXT_PUBLIC_DEBUG=true
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=<your_key>
CLERK_SECRET_KEY=<your_secret>
API_BASE_URL=http://localhost:8000
```

To get your Clerk key and secret:

- go to Clerk dashboard: https://dashboard.clerk.com/
- select the "AskWizz" organisation
- go to "API Keys"
- check that you are using the "Development" instance (top bar)
- copy the content from the `.env.local` box.

Install dependencies

```console
$ yarn install
```

Start server

```console
$ yarn dev
```

Preview is available at http://localhost:3000.

