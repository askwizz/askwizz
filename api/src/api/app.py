import urllib.parse

import dotenv
import requests
from fastapi import FastAPI, Request, Response
from fastapi.responses import RedirectResponse

from api.settings import AppSettings


def create_app() -> FastAPI:
    dotenv.load_dotenv()
    app_settings = AppSettings()
    app = FastAPI()

    @app.get("/api/connect/atlassian")
    async def oauth_start(request: Request) -> Response:
        oauth_callback_url = request.url_for(oauth_callback.__name__)
        authorization_host = "auth.atlassian.com"
        authorization_path = "/authorize"
        authorization_query_parameters = {
            "audience": "api.atlassian.com",
            "client_id": app_settings.oauth_atlassian.client_id,
            "scope": " ".join(
                [
                    # to get a refresh token
                    "offline_access",
                    # common
                    "read:me",
                    # confluence
                    "read:confluence-space.summary",
                    "read:confluence-props",
                    "read:confluence-content.all",
                    "read:confluence-content.summary",
                    "search:confluence",
                    "read:confluence-content.permission",
                    "read:confluence-user",
                    "read:confluence-groups",
                    "readonly:content.attachment:confluence",
                ]
            ),
            "redirect_uri": oauth_callback_url,
            # TODO add state in HTTP cookie-based session
            "state": "test",
            "response_type": "code",
            "prompt": "consent",
        }
        authorization_url = str(
            urllib.parse.urlunparse(
                urllib.parse.ParseResult(
                    scheme="https",
                    netloc=authorization_host,
                    path=authorization_path,
                    query=urllib.parse.urlencode(authorization_query_parameters),
                    fragment="",
                    params="",
                )
            )
        )

        print(authorization_url)

        return RedirectResponse(url=authorization_url)

    @app.get("/api/connect/atlassian/callback")
    async def oauth_callback(request: Request, state: str, code: str):
        # TODO check state in HTTP cookie-based session
        oauth_callback_url = request.url_for(oauth_callback.__name__)
        token_host = "auth.atlassian.com"
        token_path = "/oauth/token"
        token_payload: dict[str, str] = {
            "grant_type": "authorization_code",
            "client_id": app_settings.oauth_atlassian.client_id,
            "client_secret": app_settings.oauth_atlassian.client_secret,
            "code": code,
            "redirect_uri": str(oauth_callback_url),
        }

        token_url = str(
            urllib.parse.urlunparse(
                urllib.parse.ParseResult(
                    scheme="https",
                    netloc=token_host,
                    path=token_path,
                    query="",
                    fragment="",
                    params="",
                )
            )
        )

        token_response = requests.post(url=token_url, json=token_payload)

        try:
            token_response.raise_for_status()
            token_response_json = token_response.json()
        except (requests.HTTPError, requests.JSONDecodeError) as e:
            raise Exception("Bad response from OAuth server") from e

        # TODO store to database
        print(token_response_json)

        # TODO redirect proper result or error message
        return RedirectResponse(url="/")

    return app
