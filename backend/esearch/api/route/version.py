from fastapi import FastAPI

VERSION = "0.0.1"


def add_routes(app: FastAPI) -> None:
    @app.get("/api/version")
    async def version() -> str:
        return VERSION
