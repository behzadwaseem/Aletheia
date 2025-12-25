import numpy as np
import torch
from typing import Dict, List, Tuple


@torch.no_grad()
def rank_items(
    model: torch.nn.Module,
    user_id: int,
    item_ids: List[int],
    device: torch.device,
) -> np.ndarray:
    """
    Returns item_ids sorted by descending score.
    """
    users = torch.tensor([user_id] * len(item_ids), device=device)
    items = torch.tensor(item_ids, device=device)

    scores = model(users, items)
    scores = scores.cpu().numpy()

    ranked_indices = np.argsort(-scores)
    return np.array(item_ids)[ranked_indices]


def hit_at_k(ranked_items: np.ndarray, true_item: int, k: int) -> int:
    return int(true_item in ranked_items[:k])


def ndcg_at_k(ranked_items: np.ndarray, true_item: int, k: int) -> float:
    if true_item not in ranked_items[:k]:
        return 0.0
    rank = np.where(ranked_items == true_item)[0][0] + 1
    return 1.0 / np.log2(rank + 1)
