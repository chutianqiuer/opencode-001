from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from loguru import logger

from app.config import settings
from app.database import init_db
from app.middleware.cors import setup_cors
from app.middleware.logging import LoggingMiddleware, setup_logging
from app.utils.redis_client import redis_client
from app.routers import auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")

    await redis_client.connect()
    logger.info("Redis connected")

    await init_db()
    logger.info("Database initialized")

    yield

    await redis_client.disconnect()
    logger.info("Redis disconnected")
    logger.info(f"Shutting down {settings.APP_NAME}")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

setup_cors(app)

app.add_middleware(LoggingMiddleware)

app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

app.include_router(auth.router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.APP_VERSION}


@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "docs": "/docs",
        "version": settings.APP_VERSION,
    }
