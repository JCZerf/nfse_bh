from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

load_dotenv()

from api.exception_handlers import validation_exception_handler
from api.rate_limit import limiter
from api.routes.health import router as health_router
from api.routes.metrics import router as metrics_router
from api.routes.nfse import router as nfse_router

app = FastAPI(title="NFS-e BH Collector")
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.include_router(nfse_router)
app.include_router(health_router)
app.include_router(metrics_router)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
