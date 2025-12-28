from fastapi import APIRouter, Request

router = APIRouter()

@router.get("health")
def health(request: Request):
    return {
        "status": "ok",
        "model_loaded": hasattr(request.app.state, "recommender"),
    }
