#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api.routers import v1
from app.common.log import log
from app.common.redis import redis_client
from app.common.task import scheduler
from app.core.conf import settings


@asynccontextmanager
async def startup_init(app: FastAPI):
    await redis_client.aopen()
    scheduler.start()

    yield

    await redis_client.aclose()
    scheduler.shutdown()


app = FastAPI(
    title=settings.TITLE,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOCS_URL,
    openapi_url=settings.OPENAPI_URL,
    lifespan=startup_init,
)

app.include_router(v1)

if __name__ == '__main__':
    try:
        log.info(
            """\n
 /$$$$$$$$                   /$$      /$$$$$$  /$$$$$$$  /$$$$$$
| $$_____/                  | $$     /$$__  $$| $$__  $$|_  $$_/
| $$    /$$$$$$   /$$$$$$$ /$$$$$$  | $$  | $$| $$  | $$  | $$  
| $$$$$|____  $$ /$$_____/|_  $$_/  | $$$$$$$$| $$$$$$$/  | $$  
| $$__/ /$$$$$$$|  $$$$$$   | $$    | $$__  $$| $$____/   | $$  
| $$   /$$__  $$ |____  $$  | $$ /$$| $$  | $$| $$        | $$  
| $$  |  $$$$$$$ /$$$$$$$/  |  $$$$/| $$  | $$| $$       /$$$$$$
|__/   |_______/|_______/    |___/  |__/  |__/|__/      |______/

            """
        )
        uvicorn.run(
            app='main:app',
            host=settings.UVICORN_HOST,
            port=settings.UVICORN_PORT,
            reload=settings.UVICORN_RELOAD,
        )
    except Exception as e:
        log.error(f'❌ FastAPI start filed: {e}')
