from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

from api.routes.nfse import router as nfse_router

app = FastAPI(title="NFS-e BH Collector")
app.include_router(nfse_router)
