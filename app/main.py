import logging
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app import labels, model_service
from app.routers import health, metadata, predict
from app.settings import settings

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    model_service.load()
    model_service.warmup()

    missing = labels.untranslated_values(model_service.category_options())
    if missing:
        logger.warning("Category values with no English label: %s", missing)

    yield
    model_service.unload()


app = FastAPI(
    title="Used car valuation",
    description=(
        "API for valuing used cars, based on an XGBoost model trained on "
        "listings from the Polish market."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())[:8]
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    fields = []
    for error in exc.errors():
        location = [str(part) for part in error["loc"] if part != "body"]
        fields.append({"field": ".".join(location) or "(request body)", "message": error["msg"]})

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"error": "Invalid input data", "fields": fields},
    )


@app.exception_handler(Exception)
async def unhandled_error_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", "-")
    logger.exception("Unhandled error (request_id=%s)", request_id)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error", "request_id": request_id},
    )


app.include_router(health.router)
app.include_router(metadata.router)
app.include_router(predict.router)

app.mount("/", StaticFiles(directory=settings.static_dir, html=True), name="static")
