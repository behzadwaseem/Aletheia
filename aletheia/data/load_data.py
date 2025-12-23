import pandas as pd
from pathlib import Path

def load_movielens(path: Path) -> pd.DataFrame:
    cols = ["user_id", "movie_id", "rating", "timestamp"]
    df = pd.read_csv(
        path / "u.data",
        sep="\t",
        names=cols
    )

    # Normalize naming
    df = df.rename(columns={"movie_id": "item_id"})
    
    return df