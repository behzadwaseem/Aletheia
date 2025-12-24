from pathlib import Path
import pandas as pd
import torch

from aletheia.data.load_data import load_movielens
from aletheia.data.interactions import to_implicit
from aletheia.utils.sampling import negative_sample
from aletheia.training.train_config import TrainConfig
from aletheia.training.train import train


DATA_DIR = Path("data/ml-100k")


def main():
    df = load_movielens(DATA_DIR)

    # IMPORTANT: IDs should be contiguous ints for embeddings.
    # If user_id/item_id are not already 0..N-1, we remap them here.
    user_map = {u: i for i, u in enumerate(sorted(df["user_id"].unique()))}
    item_map = {m: i for i, m in enumerate(sorted(df["item_id"].unique()))}

    df = df.copy()
    df["user_id"] = df["user_id"].map(user_map)
    df["item_id"] = df["item_id"].map(item_map)

    positives = to_implicit(df, min_rating=4)

    num_users = len(user_map)
    num_items = len(item_map)

    negatives = negative_sample(
        positives=positives,
        num_items=num_items,
        negatives_per_positive=4,
        seed=42,
    )

    interactions = pd.concat([positives, negatives], ignore_index=True)

    cfg = TrainConfig(
        embedding_dim=64,
        hidden_dims=[128, 64],
        batch_size=2048,
        lr=1e-3,
        epochs=3,
        device="cuda" if torch.cuda.is_available() else "cpu",
        log_every=200,
    )

    model = train(interactions, num_users=num_users, num_items=num_items, cfg=cfg)

    # Optional: save checkpoint
    Path("checkpoints").mkdir(exist_ok=True)
    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "num_users": num_users,
            "num_items": num_items,
            "user_map": user_map,
            "item_map": item_map,
            "config": cfg.__dict__,
        },
        "checkpoints/ncf.pt",
    )
    print("Saved checkpoint to checkpoints/ncf.pt")


if __name__ == "__main__":
    main()
