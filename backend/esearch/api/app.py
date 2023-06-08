import dotenv
from fastapi import FastAPI

import esearch.api.route.auth
import esearch.api.route.connection
import esearch.api.route.indexing
import esearch.api.route.search
from esearch.api.lifespan import get_lifespan
from esearch.api.settings import AppSettings
from esearch.db.engine import Base, engine

Base.metadata.create_all(bind=engine)


def create_app_with_settings(app_settings: AppSettings) -> FastAPI:
    app = FastAPI()

    app.router.lifespan_context = get_lifespan(app_settings)
    esearch.api.route.auth.add_routes(app=app, app_settings=app_settings)
    esearch.api.route.search.add_routes(app=app)
    esearch.api.route.indexing.add_routes(app=app)
    esearch.api.route.connection.add_routes(app=app)

    return app


def create_app() -> FastAPI:
    dotenv.load_dotenv()
    app_settings = AppSettings()

    return create_app_with_settings(app_settings=app_settings)
