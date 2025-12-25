import random
import numpy as np
import pandas as pd
import torch
from pathlib import Path

from aletheia.evaluation.ranking import hit_at_k, ndcg_at_k, rank_items
from aletheia.models.ncf import NeuralCollaborativeFiltering
from aletheia.data.load_data import load_movielens
from aletheia.data.interactions import to_implicit
from aletheia.utils.sampling import build_user_item_sets


DATA_DIR = Path("data/ml-100k")
NEGATIVE_SAMPLES = 99
K = 10


def main():
    checkpoint = torch.load("checkpoints/ncf.pt", weights_only=False)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = NeuralCollaborativeFiltering(
        checkpoint["num_users"],
        checkpoint["num_items"],
    )
    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(device)
    model.eval()

    df = load_movielens(DATA_DIR)
    df["user_id"] = df["user_id"].map(checkpoint["user_map"])
    df["item_id"] = df["item_id"].map(checkpoint["item_map"])

    positives = to_implicit(df)
    user_item_sets = build_user_item_sets(positives)

    hits, ndcgs = [], []

    for user, items in user_item_sets.items():
        true_item = random.choice(list(items))

        negatives = []
        while len(negatives) < NEGATIVE_SAMPLES:
            neg = random.randint(0, checkpoint["num_items"] - 1)
            if neg not in items:
                negatives.append(neg)

        candidates = negatives + [true_item]
        ranked = rank_items(model, user, candidates, device)

        hits.append(hit_at_k(ranked, true_item, K))
        ndcgs.append(ndcg_at_k(ranked, true_item, K))

    print(f"Hit@{K}:  {np.mean(hits):.4f}")
    print(f"NDCG@{K}: {np.mean(ndcgs):.4f}")


if __name__ == "__main__":
    main()
