import torch
from torch.utils.data import Dataset
import pandas as pd


class InteractionDataset(Dataset):
    def __init__(self, interactions: pd.DataFrame):
        self.users = torch.tensor(
            interactions["user_id"].values, dtype=torch.long
        )
        self.items = torch.tensor(
            interactions["item_id"].values, dtype=torch.long
        )
        self.labels = torch.tensor(
            interactions["label"].values, dtype=torch.float32
        )

    def __len__(self) -> int:
        return len(self.labels)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        return {
            "user": self.users[idx],
            "item": self.items[idx],
            "label": self.labels[idx],
        }
