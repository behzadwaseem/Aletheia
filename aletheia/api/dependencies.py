import torch
from pathlib import Path
import json
from pathlib import Path

from aletheia.models.ncf import NeuralCollaborativeFiltering

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
MOVIES_CSV = DATA_DIR / "movies.csv"


class RecommenderState:
    def __init__(
        self,
        model: NeuralCollaborativeFiltering,
        item_embeddings: torch.Tensor,
        item_metadata: dict,
    ):
        self.model = model
        self.item_embeddings = item_embeddings   # shape: (num_items, d)
        self.item_metadata = item_metadata       # item_id -> metadata



def load_model(checkpoint_path: Path, device: torch.device):
    checkpoint = torch.load(checkpoint_path, map_location=device)

    model = NeuralCollaborativeFiltering(
        num_users=checkpoint["num_users"],
        num_items=checkpoint["num_items"],
        embedding_dim=checkpoint["embedding_dim"],
    )

    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(device)
    model.eval()

    return model


def extract_item_embeddings(
    model: NeuralCollaborativeFiltering,
) -> torch.Tensor:
    """
    Returns item embedding matrix of shape (num_items, embedding_dim)
    """
    with torch.no_grad():
        return model.item_embedding.weight.detach().clone()



def load_item_metadata(path: Path) -> dict:
    """
    Returns: item_id -> {title, genres}
    """
    metadata = {}

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            movie_id, title, genres = line.strip().split(",", 2)
            metadata[int(movie_id)] = {
                "title": title,
                "genres": genres.split("|"),
            }

    return metadata


def load_recommender_state() -> RecommenderState:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = load_model(
        checkpoint_path=Path("checkpoints/ncf.pt"),
        device=device,
    )

    item_embeddings = extract_item_embeddings(model)

    item_metadata = load_item_metadata(MOVIES_CSV)

    return RecommenderState(
        model=model,
        item_embeddings=item_embeddings,
        item_metadata=item_metadata,
    )
