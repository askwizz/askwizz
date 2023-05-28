import dotenv
from fastapi import FastAPI

import api.route.auth
from api.settings import AppSettings


def create_app() -> FastAPI:
    dotenv.load_dotenv()
    app_settings = AppSettings()
    app = FastAPI()

    api.route.auth.add_routes(app=app, app_settings=app_settings)

    return app
