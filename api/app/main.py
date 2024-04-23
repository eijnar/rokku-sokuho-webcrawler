# app/main.py

from fastapi import FastAPI, APIRouter
from .api.endpoints import bands, urls
from .database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

base_router = APIRouter(prefix="/v1")
base_router.include_router(bands.router)
base_router.include_router(urls.router)

app.include_router(base_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
