import logging

import dotenv
from fastapi import FastAPI

import esearch.api.route.answer
import esearch.api.route.auth
import esearch.api.route.connection
import esearch.api.route.history
import esearch.api.route.search
import esearch.api.route.version
from esearch.api.lifespan import get_lifespan
from esearch.api.settings import AppSettings


def create_app_with_settings(app_settings: AppSettings) -> FastAPI:
    app = FastAPI()

    app.router.lifespan_context = get_lifespan(app_settings)
    esearch.api.route.auth.add_routes(app=app, app_settings=app_settings)
    esearch.api.route.search.add_routes(app=app, settings=app_settings)
    esearch.api.route.connection.add_routes(app=app, settings=app_settings)
    esearch.api.route.history.add_routes(app=app, settings=app_settings)
    esearch.api.route.answer.add_routes(app=app, settings=app_settings)
    esearch.api.route.version.add_routes(app=app)
    logging.warning("Configured routes")

    return app


def create_app() -> FastAPI:
    logging.basicConfig(level=logging.INFO)
    dotenv.load_dotenv()
    app_settings = AppSettings()

    return create_app_with_settings(app_settings=app_settings)
