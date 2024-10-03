from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.models import db_helper
from app.api.api_v1 import kittens

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


app = FastAPI(
    lifespan=lifespan,
)
app.include_router(kittens.router)