from fastapi import FastAPI
from contextlib import asynccontextmanager

from aletheia.api.router import api_v1_router
from aletheia.api.dependencies import load_recommender_state


@asynccontextmanager
async def lifespan(app: FastAPI): # startup event
    print("Loading recommender model...")
    app.state.recommender = load_recommender_state()
    print("Model loaded.")
    yield
    print("Shutting down.")


app = FastAPI(
    title="Aletheia",
    version="0.1.0",
    lifespan=lifespan
)


app.include_router(
    api_v1_router
)


@app.get("/")
def read_root():
    return {"message": "Welcome to Aletheia!"}



