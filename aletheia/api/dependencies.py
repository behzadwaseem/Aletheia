import torch
from pathlib import Path

from aletheia.models.ncf import NeuralCollaborativeFiltering


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
U_ITEM_PATH = DATA_DIR / "ml-100k/u.item"
CHECKPOINT_PATH = PROJECT_ROOT / "checkpoints/ncf.pt"

GENRE_NAMES = [
    "unknown",
    "Action",
    "Adventure",
    "Animation",
    "Children",
    "Comedy",
    "Crime",
    "Documentary",
    "Drama",
    "Fantasy",
    "Film-Noir",
    "Horror",
    "Musical",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Thriller",
    "War",
    "Western",
]


class RecommenderState:
    def __init__(
        self,
        model: NeuralCollaborativeFiltering,
        item_embeddings: torch.Tensor,
        item_metadata: dict,
        item2idx: dict,
        idx2item: dict,
    ):
        self.model = model
        self.item_embeddings = item_embeddings   # (num_items, d)
        self.item_metadata = item_metadata       # raw_movie_id -> metadata
        self.item2idx = item2idx                 # raw_movie_id -> index
        self.idx2item = idx2item                 # index -> raw_movie_id


def load_model(checkpoint_path: Path, device: torch.device):
    """
    Load a trained NCF model from a checkpoint and prepare it for inference.

    Reconstructs the model architecture, loads weights, moves the model to
    the specified device, and sets evaluation mode.
    """
    checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)

    model = NeuralCollaborativeFiltering(
        num_users=checkpoint["num_users"],
        num_items=checkpoint["num_items"],
        # embedding_dim=checkpoint["embedding_dim"],
    )

    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(device)
    model.eval()

    return model


def extract_item_embeddings(model: NeuralCollaborativeFiltering) -> torch.Tensor:
    """
    Load MovieLens 100K movie metadata from the u.item file.

    Parses binary genre flags into human-readable genres and returns
    metadata keyed by raw MovieLens movie IDs.
    """

    with torch.no_grad():
        return model.item_embedding.weight.detach().clone()


def load_item_metadata(path: Path):
    """
    Load MovieLens 100K movie metadata from the u.item file.

    Parses binary genre flags into human-readable genres and returns
    metadata keyed by raw MovieLens movie IDs.
    """
    metadata = {}
    item_ids = []

    with open(path, encoding="latin-1") as f:
        for line in f:
            parts = line.strip().split("|")

            movie_id = int(parts[0])
            title = parts[1]
            genre_flags = parts[5:]  # 19 binary flags

            genres = [
                genre
                for genre, flag in zip(GENRE_NAMES, genre_flags)
                if flag == "1"
            ]

            metadata[movie_id] = {
                "title": title,
                "genres": genres,
            }
            item_ids.append(movie_id)

    return metadata, item_ids


def load_recommender_state() -> RecommenderState:
    """
    Initialize the shared recommender inference state.

    Loads the trained model, item embeddings, metadata, and builds explicit
    ID-to-index mappings to ensure correct embedding lookup at inference time.
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = load_model(
        checkpoint_path=CHECKPOINT_PATH,
        device=device,
    )

    item_embeddings = extract_item_embeddings(model)

    item_metadata, item_ids = load_item_metadata(U_ITEM_PATH)

    # Build ID ↔ index mappings
    item2idx = {item_id: idx for idx, item_id in enumerate(item_ids)}
    idx2item = {idx: item_id for item_id, idx in item2idx.items()}

    # Critical sanity check
    assert item_embeddings.size(0) == len(item2idx), (
        "Mismatch between embedding matrix size and item ID mapping"
    )

    print("Num items:", item_embeddings.size(0))
    print("Num metadata entries:", len(item_metadata))

    return RecommenderState(
        model=model,
        item_embeddings=item_embeddings,
        item_metadata=item_metadata,
        item2idx=item2idx,
        idx2item=idx2item,
    )
