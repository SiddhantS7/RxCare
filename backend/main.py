import warnings
warnings.filterwarnings("ignore")
from fastapi import FastAPI
from backend.api.prescription import router as prescription_router

app = FastAPI(title="RxCare API")

app.include_router(prescription_router)

@app.get("/")
def root():
    return {"status": "RxCare backend running"}
