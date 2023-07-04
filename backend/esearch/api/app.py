import logging

import dotenv
import uvicorn.logging
from fastapi import FastAPI

import esearch.api.route.auth
import esearch.api.route.connection
import esearch.api.route.search
import esearch.api.route.version
from esearch.api.lifespan import get_lifespan
from esearch.api.settings import AppSettings


def create_app_with_settings(app_settings: AppSettings) -> FastAPI:
    app = FastAPI()

    app.router.lifespan_context = get_lifespan(app_settings)
    esearch.api.route.auth.add_routes(app=app, app_settings=app_settings)
    esearch.api.route.search.add_routes(app=app)
    esearch.api.route.connection.add_routes(app=app, settings=app_settings)
    esearch.api.route.version.add_routes(app=app)

    return app


def create_app() -> FastAPI:
    logging_handler = logging.StreamHandler()
    logging_handler.setFormatter(uvicorn.logging.DefaultFormatter())
    logging.getLogger().addHandler(logging_handler)
    dotenv.load_dotenv()
    app_settings = AppSettings()

    return create_app_with_settings(app_settings=app_settings)
