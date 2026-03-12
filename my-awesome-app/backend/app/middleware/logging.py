import time
from fastapi import Request, Response
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        request_id = f"{time.time_ns()}"

        logger.info(
            f"[{request_id}] Request: {request.method} {request.url.path} "
            f"Client: {request.client.host if request.client else 'unknown'}"
        )

        try:
            response: Response = await call_next(request)
            process_time = (time.time() - start_time) * 1000

            logger.info(
                f"[{request_id}] Response: {response.status_code} Duration: {process_time:.2f}ms"
            )

            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = f"{process_time:.2f}ms"

            return response

        except Exception as e:
            process_time = (time.time() - start_time) * 1000
            logger.error(f"[{request_id}] Error: {str(e)} Duration: {process_time:.2f}ms")
            raise


def setup_logging():
    logger.add(
        "logs/app.log",
        rotation="10 MB",
        retention="7 days",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    )
