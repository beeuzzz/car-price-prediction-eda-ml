import logging
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app import model_service
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
    yield
    model_service.unload()


app = FastAPI(
    title="Wycena pojazdów używanych",
    description=(
        "API wyceny samochodów używanych na podstawie modelu XGBoost "
        "wytrenowanego na ogłoszeniach z polskiego rynku."
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
    """Domyślny format Pydantic jest nieczytelny dla frontendu - spłaszczamy go do
    listy {pole, komunikat}, żeby dało się podpiąć błąd pod konkretne pole formularza."""
    fields = []
    for error in exc.errors():
        location = [str(part) for part in error["loc"] if part != "body"]
        fields.append({"pole": ".".join(location) or "(treść żądania)", "komunikat": error["msg"]})

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"blad": "Nieprawidłowe dane wejściowe", "pola": fields},
    )


@app.exception_handler(Exception)
async def unhandled_error_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", "-")
    logger.exception("Nieobsłużony błąd (request_id=%s)", request_id)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"blad": "Błąd wewnętrzny serwera", "request_id": request_id},
    )


app.include_router(health.router)
app.include_router(metadata.router)
app.include_router(predict.router)

app.mount("/", StaticFiles(directory=settings.static_dir, html=True), name="static")
