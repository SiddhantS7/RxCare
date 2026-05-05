from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ FIRST create app
app = FastAPI()

# ✅ THEN add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ THEN import routers
from backend.api.prescription import router as prescription_router

app.include_router(prescription_router)

# optional test route
@app.get("/")
def root():
    return {"message": "RxCare API running"}