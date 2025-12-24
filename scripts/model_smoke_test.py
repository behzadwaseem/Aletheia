import torch
from aletheia.models.ncf import NeuralCollaborativeFiltering

num_users = 100
num_items = 500

model = NeuralCollaborativeFiltering(num_users, num_items)

users = torch.tensor([1, 5, 10])
items = torch.tensor([20, 33, 42])

scores = model(users, items)
print(scores)
print(scores.shape)