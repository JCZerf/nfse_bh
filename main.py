from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

from api.routes.health import router as health_router
from api.routes.metrics import router as metrics_router
from api.routes.nfse import router as nfse_router

app = FastAPI(title="NFS-e BH Collector")
app.include_router(nfse_router)
app.include_router(health_router)
app.include_router(metrics_router)
