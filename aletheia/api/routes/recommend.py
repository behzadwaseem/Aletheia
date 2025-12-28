from fastapi import APIRouter, Request, HTTPException
from aletheia.api.schemas import PreferenceRequest

import torch

router = APIRouter()


@router.post("/recommendations/preferences")
def recommend_from_preferences(
    req: PreferenceRequest,
    request: Request,
):
    state = request.app.state.recommender

    embeddings = state.item_embeddings
    metadata = state.item_metadata

    missing = [i for i in req.item_ids if i >= embeddings.size(0)]
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown item_ids: {missing}",
        )

    # Aggregate embeddings
    selected = embeddings[req.item_ids]
    user_pref = selected.mean(dim=0)

    # Dot product scoring
    scores = embeddings @ user_pref

    for i in req.item_ids:
        scores[i] = -float("inf")

    top_k = torch.topk(scores, req.k)

    recommendations = []
    for rank, item_id in enumerate(top_k.indices.tolist(), start=1):
        meta = metadata[item_id]
        recommendations.append({
            "item_id": item_id,
            "title": meta["title"],
            "genres": meta["genres"],
            "score": top_k.values[rank - 1].item(),
            "rank": rank,
        })

    return {
        "input_items": [
            {
                "item_id": i,
                "title": metadata[i]["title"],
            }
            for i in req.item_ids
        ],
        "recommendations": recommendations,
    }