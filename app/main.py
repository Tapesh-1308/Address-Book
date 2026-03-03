from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.session import engine
from app.db.base import Base
from app.api.routes import router as address_router
from app.core.logging import setup_logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Address Book API",
    lifespan=lifespan
)

app.include_router(address_router)