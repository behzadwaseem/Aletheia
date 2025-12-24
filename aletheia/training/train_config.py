from dataclasses import dataclass

@dataclass
class TrainConfig:
    embedding_dim: int = 64
    hidden_dims: list[int] = None
    batch_size: int = 2048
    lr: float = 1e-3
    epochs: int = 3
    device: str = "cpu"
    log_every: int = 100
    negative_weight: float = 0.1

    def __post_init__(self):
        if self.hidden_dims is None:
            self.hidden_dims = [128, 64]