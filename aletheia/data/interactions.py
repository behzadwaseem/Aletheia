import pandas as pd

def to_implicit(df: pd.DataFrame, min_rating: int = 4) -> pd.DataFrame:
    """
    Converts explicit ratings into implicit positive interactions by thresholding 
    high-confidence user-item signals and preparing them for negative sampling
    and ranking-based training.

    Uses min_rating as the cut-off for positive interactions.
    """
    df = df[df["rating"] >= min_rating].copy()
    df["label"] = 1
    return df[["user_id", "item_id", "label"]]