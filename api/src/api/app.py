import dotenv
from fastapi import FastAPI

import api.route.auth
import api.route.search
from api.settings import AppSettings


def create_app_with_settings(app_settings: AppSettings) -> FastAPI:
    app = FastAPI()

    api.route.auth.add_routes(app=app, app_settings=app_settings)
    api.route.search.add_routes(app=app, app_settings=app_settings)

    return app


def create_app() -> FastAPI:
    dotenv.load_dotenv()
    app_settings = AppSettings()

    return create_app_with_settings(app_settings=app_settings)
