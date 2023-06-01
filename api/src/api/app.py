import dotenv
from fastapi import FastAPI

import api.route.auth
import api.route.indexing
import api.route.search
from api.lifespan import get_lifespan
from api.settings import AppSettings


def create_app_with_settings(app_settings: AppSettings) -> FastAPI:
    app = FastAPI()

    app.router.lifespan_context = get_lifespan(app_settings)
    api.route.auth.add_routes(app=app, app_settings=app_settings)
    api.route.search.add_routes(app=app)
    api.route.indexing.add_routes(app=app)

    return app


def create_app() -> FastAPI:
    dotenv.load_dotenv()
    app_settings = AppSettings()

    return create_app_with_settings(app_settings=app_settings)
