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

    embeddings = state.item_embeddings         # (num_items, d)
    item2idx = state.item2idx                  # raw_id -> index
    idx2item = state.idx2item                  # index -> raw_id
    metadata = state.item_metadata             # raw_id -> metadata

    # Validate item IDs
    missing = [i for i in req.item_ids if i not in item2idx]
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown item_ids: {missing}",
        )
    
    # Map raw IDs -> indices
    item_indices = torch.tensor(
        [item2idx[i] for i in req.item_ids],
        dtype=torch.long,
    )

    # Aggregate embeddings
    selected = embeddings[item_indices]         # (n_selected, d)
    user_pref = selected.mean(dim=0)            # (d,)

    # Score all items
    scores = (embeddings @ user_pref).clone()   # (num_items,)

    # Exclude selected items
    scores[item_indices] = -float("inf")

    # Top-K ranking
    k = min(req.k, scores.size(0) - len(item_indices))
    values, indices = torch.topk(scores, k)

    # Build response
    recommendations = []
    for rank, (idx, score) in enumerate(zip(indices.tolist(), values.tolist()), start=1):
        raw_id = idx2item[idx]
        meta = metadata[raw_id]

        recommendations.append({
            "item_id": raw_id,
            "title": meta["title"],
            "genres": meta["genres"],
            "score": score,
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