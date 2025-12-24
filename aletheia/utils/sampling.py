import numpy as np
import pandas as pd
from typing import Dict, Set

def build_user_item_sets(df: pd.DataFrame) -> Dict[int, Set[int]]:
    """
    Builds a mapping from user_id -> set of interacted item_ids.
    """
    user_items = {}
    
    # add all users and items they've interacted with to the dict
    for row in df.itertuples():
        user_items.setdefault(row.user_id, set()).add(row.item_id)
    return user_items


def negative_sample(
        positives: pd.DataFrame,
        num_items: int,
        negatives_per_positive: int=4,
        seed: int = 42,
) -> pd.DataFrame:
    """
    For each positive interaction, sample N negative items
    the user has not interacted with.
    """
    rng = np.random.default_rng(seed)

    user_item_sets = build_user_item_sets(positives)
    rows = []

    for row in positives.itertuples():
        user = row.user_id
        positives_for_user = user_item_sets[user]

        for _ in range(negatives_per_positive):
            neg_item = rng.integers(0, num_items)

            while neg_item in positives_for_user:
                neg_item = rng.integers(0, num_items)

            rows.append((user, neg_item, 0))

    negatives = pd.DataFrame(rows, columns=["user_id", "item_id", "label"])
    return negatives