from __future__ import annotations

import time
import pandas as pd
import torch
from torch.utils.data import DataLoader

from aletheia.models.ncf import NeuralCollaborativeFiltering
from aletheia.training.train_config import TrainConfig
from aletheia.training.dataset import InteractionDataset


def train_one_epoch(
    model: torch.nn.Module,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    loss_fn: torch.nn.Module,
    device: torch.device,
    negative_weight: float,
    log_every: int = 100
) -> float:
    model.train()
    running_loss = 0.0
    n_examples = 0
    start = time.time()

    for step, batch in enumerate(loader, start=1):
        users = batch["user"].to(device)
        items = batch["item"].to(device)
        labels = batch["label"].to(device)

        optimizer.zero_grad(set_to_none=True)

        # Per-example BCE loss
        logits = model(users, items)                 # shape: (batch,)
        losses = loss_fn(logits, labels)   # shape: (batch,)

        # Build weights: positives=1.0, negatives=negative_weight
        weights = torch.ones_like(labels)
        weights[labels == 0] = negative_weight

        # Weighted mean loss
        loss = (losses * weights).mean()

        loss.backward()
        optimizer.step()

        bs = labels.size(0)
        running_loss += loss.item() * bs
        n_examples += bs

        if log_every and step % log_every == 0:
            elapsed = time.time() - start
            avg = running_loss / max(n_examples, 1)
            print(f"  step {step:>5} | avg_loss={avg:.4f} | {n_examples/elapsed:,.0f} ex/s")

    return running_loss / max(n_examples, 1)



def train(
    interactions: pd.DataFrame,
    num_users: int,
    num_items: int,
    cfg: TrainConfig,
) -> NeuralCollaborativeFiltering:
    device = torch.device(cfg.device)

    dataset = InteractionDataset(interactions)
    loader = DataLoader(
        dataset,
        batch_size=cfg.batch_size,
        shuffle=True,
        num_workers=0,          # set >0 later if you want
        pin_memory=(device.type == "cpu"),
    )

    model = NeuralCollaborativeFiltering(
        num_users=num_users,
        num_items=num_items,
        embedding_dim=cfg.embedding_dim,
        hidden_dims=cfg.hidden_dims,
    ).to(device)

    loss_fn = torch.nn.BCEWithLogitsLoss(reduction="none")
    optimizer = torch.optim.Adam(model.parameters(), lr=cfg.lr)

    print(f"Training on {device} | examples={len(dataset):,} | batch_size={cfg.batch_size}")
    for epoch in range(1, cfg.epochs + 1):
        avg_loss = train_one_epoch(model, loader, optimizer, loss_fn, device, cfg.negative_weight, cfg.log_every)
        print(f"epoch {epoch}/{cfg.epochs} | loss={avg_loss:.4f}")

    return model